import { useState } from 'react';
import { ChevronDown, ChevronUp, User, Bot, FileSearch } from 'lucide-react';
import SourceCard from './SourceCard';

export default function Message({ message, isUser }) {
    const [showSources, setShowSources] = useState(false);
    const [showPrompt, setShowPrompt] = useState(false);

    if (isUser) {
        return (
            <div className="flex justify-end mb-4 animate-fade-in">
                <div className="flex items-start gap-3 max-w-[80%]">
                    <div className="chat-bubble chat-bubble-user">
                        {message.content}
                    </div>
                    <div className="p-2 bg-primary-600 rounded-full flex-shrink-0">
                        <User className="w-4 h-4 text-white" />
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="flex justify-start mb-4 animate-fade-in">
            <div className="flex items-start gap-3 max-w-[85%]">
                <div className="p-2 bg-slate-700 rounded-full flex-shrink-0">
                    <Bot className="w-4 h-4 text-primary-400" />
                </div>

                <div className="flex-1">
                    <div className="chat-bubble chat-bubble-assistant">
                        {message.content}
                    </div>

                    {/* Confidence Score */}
                    {message.confidence !== undefined && (
                        <div className="mt-2 flex items-center gap-2 text-xs text-slate-400">
                            <span>Confidence:</span>
                            <div className="flex-1 max-w-[100px] h-1.5 bg-slate-800 rounded-full overflow-hidden">
                                <div
                                    className="h-full bg-primary-500 transition-all duration-300"
                                    style={{ width: `${message.confidence * 100}%` }}
                                />
                            </div>
                            <span>{(message.confidence * 100).toFixed(1)}%</span>
                        </div>
                    )}

                    {/* Sources Toggle */}
                    {message.sources && message.sources.length > 0 && (
                        <div className="mt-3">
                            <button
                                onClick={() => setShowSources(!showSources)}
                                className="flex items-center gap-2 text-sm text-primary-400 hover:text-primary-300 transition-colors"
                            >
                                <FileSearch className="w-4 h-4" />
                                <span>{message.sources.length} source{message.sources.length !== 1 ? 's' : ''}</span>
                                {showSources ? (
                                    <ChevronUp className="w-4 h-4" />
                                ) : (
                                    <ChevronDown className="w-4 h-4" />
                                )}
                            </button>

                            {showSources && (
                                <div className="mt-3 space-y-2">
                                    {message.sources.map((source, index) => (
                                        <SourceCard key={source.chunk_id} source={source} index={index} />
                                    ))}
                                </div>
                            )}
                        </div>
                    )}

                    {/* Developer Mode: Show Prompt */}
                    {message.prompt_used && (
                        <div className="mt-3">
                            <button
                                onClick={() => setShowPrompt(!showPrompt)}
                                className="flex items-center gap-2 text-xs text-slate-500 hover:text-slate-400 transition-colors"
                            >
                                <span>Developer Mode: View Prompt</span>
                                {showPrompt ? (
                                    <ChevronUp className="w-3 h-3" />
                                ) : (
                                    <ChevronDown className="w-3 h-3" />
                                )}
                            </button>

                            {showPrompt && (
                                <pre className="mt-2 p-3 bg-slate-950 border border-slate-800 rounded-lg text-xs text-slate-400 overflow-x-auto custom-scrollbar">
                                    {message.prompt_used}
                                </pre>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
