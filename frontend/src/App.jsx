import { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import ChatPanel from './components/ChatPanel';
import { documentAPI } from './services/api';

function App() {
    const [documents, setDocuments] = useState([]);
    const [developerMode, setDeveloperMode] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadDocuments();
    }, []);

    const loadDocuments = async () => {
        try {
            const docs = await documentAPI.list();
            setDocuments(docs);
        } catch (error) {
            console.error('Error loading documents:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="h-screen flex items-center justify-center bg-slate-950">
                <div className="text-center">
                    <div className="w-16 h-16 border-4 border-primary-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                    <p className="text-slate-400">Loading...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="flex h-screen overflow-hidden">
            <Sidebar
                documents={documents}
                onDocumentsChange={setDocuments}
                developerMode={developerMode}
                onDeveloperModeChange={setDeveloperMode}
            />
            <ChatPanel
                documents={documents}
                developerMode={developerMode}
            />
        </div>
    );
}

export default App;
