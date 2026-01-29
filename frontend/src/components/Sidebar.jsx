import { useState, useRef } from 'react';
import { Upload, FileText, Trash2, Loader2, Database, Settings } from 'lucide-react';
import { documentAPI } from '../services/api';

export default function Sidebar({ documents, onDocumentsChange, developerMode, onDeveloperModeChange }) {
    const [uploading, setUploading] = useState(false);
    const [dragActive, setDragActive] = useState(false);
    const [showInfo, setShowInfo] = useState(false);
    const [vectorInfo, setVectorInfo] = useState(null);
    const fileInputRef = useRef(null);

    const handleFileUpload = async (file) => {
        if (!file) return;

        setUploading(true);
        try {
            await documentAPI.upload(file);
            // Refresh document list
            const updatedDocs = await documentAPI.list();
            onDocumentsChange(updatedDocs);
        } catch (error) {
            console.error('Upload error:', error);
            alert(`Upload failed: ${error.response?.data?.detail || error.message}`);
        } finally {
            setUploading(false);
        }
    };

    const handleDelete = async (filename) => {
        if (!confirm(`Delete "${filename}"?`)) return;

        try {
            await documentAPI.delete(filename);
            const updatedDocs = await documentAPI.list();
            onDocumentsChange(updatedDocs);
        } catch (error) {
            console.error('Delete error:', error);
            alert(`Delete failed: ${error.response?.data?.detail || error.message}`);
        }
    };

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true);
        } else if (e.type === 'dragleave') {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    };

    const loadVectorInfo = async () => {
        try {
            const info = await documentAPI.getInfo();
            setVectorInfo(info);
            setShowInfo(true);
        } catch (error) {
            console.error('Error loading info:', error);
        }
    };

    return (
        <div className="w-80 border-r border-slate-800 bg-slate-900 flex flex-col h-screen">
            {/* Header */}
            <div className="p-6 border-b border-slate-800">
                <h2 className="text-lg font-semibold text-slate-100 mb-1">Documents</h2>
                <p className="text-sm text-slate-400">
                    {documents.length} indexed
                </p>
            </div>

            {/* Upload Area */}
            <div className="p-4 border-b border-slate-800">
                <div
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                    onClick={() => fileInputRef.current?.click()}
                    className={`
            border-2 border-dashed rounded-xl p-6 text-center cursor-pointer
            transition-all duration-200
            ${dragActive
                            ? 'border-primary-500 bg-primary-500/10'
                            : 'border-slate-700 hover:border-slate-600 hover:bg-slate-800/50'
                        }
            ${uploading ? 'opacity-50 cursor-not-allowed' : ''}
          `}
                >
                    <input
                        ref={fileInputRef}
                        type="file"
                        accept=".pdf,.docx,.txt"
                        onChange={(e) => handleFileUpload(e.target.files[0])}
                        className="hidden"
                        disabled={uploading}
                    />

                    {uploading ? (
                        <div className="flex flex-col items-center gap-2">
                            <Loader2 className="w-8 h-8 text-primary-400 animate-spin" />
                            <p className="text-sm text-slate-400">Uploading...</p>
                        </div>
                    ) : (
                        <div className="flex flex-col items-center gap-2">
                            <div className="p-3 bg-primary-600/10 rounded-xl">
                                <Upload className="w-6 h-6 text-primary-400" />
                            </div>
                            <div>
                                <p className="text-sm font-medium text-slate-200">
                                    Upload Document
                                </p>
                                <p className="text-xs text-slate-500 mt-1">
                                    PDF, DOCX, or TXT
                                </p>
                            </div>
                        </div>
                    )}
                </div>
            </div>

            {/* Document List */}
            <div className="flex-1 overflow-y-auto custom-scrollbar p-4">
                {documents.length === 0 ? (
                    <div className="text-center py-8">
                        <FileText className="w-12 h-12 text-slate-700 mx-auto mb-3" />
                        <p className="text-sm text-slate-500">No documents yet</p>
                    </div>
                ) : (
                    <div className="space-y-2">
                        {documents.map((doc, index) => (
                            <div
                                key={index}
                                className="card group hover:border-slate-700 transition-all"
                            >
                                <div className="flex items-start gap-3">
                                    <div className="p-2 bg-primary-600/10 rounded-lg flex-shrink-0">
                                        <FileText className="w-4 h-4 text-primary-400" />
                                    </div>

                                    <div className="flex-1 min-w-0">
                                        <p className="text-sm font-medium text-slate-200 truncate">
                                            {doc.filename}
                                        </p>
                                        <p className="text-xs text-slate-500 mt-0.5">
                                            {doc.num_chunks} chunks
                                        </p>
                                    </div>

                                    <button
                                        onClick={() => handleDelete(doc.filename)}
                                        className="opacity-0 group-hover:opacity-100 transition-opacity p-1.5 hover:bg-red-600/10 rounded-lg"
                                    >
                                        <Trash2 className="w-4 h-4 text-red-400" />
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Settings */}
            <div className="p-4 border-t border-slate-800 space-y-3">
                {/* Developer Mode Toggle */}
                <label className="flex items-center justify-between cursor-pointer group">
                    <span className="text-sm text-slate-300 group-hover:text-slate-200 transition-colors">
                        Developer Mode
                    </span>
                    <div className="relative">
                        <input
                            type="checkbox"
                            checked={developerMode}
                            onChange={(e) => onDeveloperModeChange(e.target.checked)}
                            className="sr-only peer"
                        />
                        <div className="w-11 h-6 bg-slate-700 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-primary-500 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                    </div>
                </label>

                {/* Vector Store Info */}
                <button
                    onClick={loadVectorInfo}
                    className="w-full btn btn-secondary flex items-center justify-center gap-2 text-sm"
                >
                    <Database className="w-4 h-4" />
                    Vector Store Info
                </button>

                {showInfo && vectorInfo && (
                    <div className="card text-xs space-y-1">
                        <div className="flex justify-between">
                            <span className="text-slate-400">Total Chunks:</span>
                            <span className="text-slate-200">{vectorInfo.total_chunks}</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-slate-400">Model:</span>
                            <span className="text-slate-200">{vectorInfo.model}</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-slate-400">Dimension:</span>
                            <span className="text-slate-200">{vectorInfo.dimension}</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-slate-400">Similarity:</span>
                            <span className="text-slate-200">{vectorInfo.similarity_metric}</span>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
