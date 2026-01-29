import { FileText, X } from 'lucide-react';

export default function SourceCard({ source, index }) {
    return (
        <div className="card text-sm animate-fade-in">
            <div className="flex items-start justify-between gap-3">
                <div className="flex items-start gap-3 flex-1">
                    <div className="p-2 bg-primary-600/10 rounded-lg">
                        <FileText className="w-4 h-4 text-primary-400" />
                    </div>

                    <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                            <span className="font-semibold text-slate-200">
                                Source {index + 1}
                            </span>
                            <span className="text-xs px-2 py-0.5 bg-primary-600/20 text-primary-300 rounded-full">
                                {(source.similarity_score * 100).toFixed(1)}% match
                            </span>
                        </div>

                        <div className="text-slate-400 text-xs mb-2">
                            {source.source}
                            {source.page && ` • Page ${source.page}`}
                        </div>

                        <p className="text-slate-300 text-sm leading-relaxed">
                            {source.text}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
