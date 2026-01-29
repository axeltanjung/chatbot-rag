import { useState, useRef, useEffect } from 'react';
import { Send, Trash2, Loader2 } from 'lucide-react';
import Message from './Message';
import { chatAPI } from '../services/api';

export default function ChatPanel({ documents, developerMode }) {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        const userMessage = {
            id: Date.now(),
            content: input,
            isUser: true,
        };

        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            // Build chat history for context
            const chatHistory = messages.map(msg => ({
                role: msg.isUser ? 'user' : 'assistant',
                content: msg.content,
            }));

            const response = await chatAPI.sendMessage(
                input,
                chatHistory,
                5,
                developerMode
            );

            const assistantMessage = {
                id: Date.now() + 1,
                content: response.answer,
                isUser: false,
                sources: response.sources,
                confidence: response.confidence,
                prompt_used: response.prompt_used,
            };

            setMessages(prev => [...prev, assistantMessage]);
        } catch (error) {
            console.error('Error sending message:', error);

            const errorMessage = {
                id: Date.now() + 1,
                content: `Error: ${error.response?.data?.detail || error.message || 'Failed to get response'}`,
                isUser: false,
                sources: [],
                confidence: 0,
            };

            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    const clearChat = () => {
        setMessages([]);
    };

    const hasDocuments = documents && documents.length > 0;

    return (
        <div className="flex flex-col h-screen bg-slate-950">
            {/* Header */}
            <div className="border-b border-slate-800 bg-slate-900/50 backdrop-blur-sm">
                <div className="px-6 py-4 flex items-center justify-between">
                    <div>
                        <h1 className="text-xl font-semibold text-slate-100">RAG Chatbot</h1>
                        <p className="text-sm text-slate-400 mt-0.5">
                            Ask questions about your documents
                        </p>
                    </div>

                    {messages.length > 0 && (
                        <button
                            onClick={clearChat}
                            className="btn btn-secondary flex items-center gap-2"
                        >
                            <Trash2 className="w-4 h-4" />
                            Clear Chat
                        </button>
                    )}
                </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto custom-scrollbar px-6 py-4">
                {messages.length === 0 ? (
                    <div className="h-full flex items-center justify-center">
                        <div className="text-center max-w-md">
                            <div className="w-16 h-16 bg-primary-600/10 rounded-2xl flex items-center justify-center mx-auto mb-4">
                                <Send className="w-8 h-8 text-primary-400" />
                            </div>
                            <h2 className="text-xl font-semibold text-slate-200 mb-2">
                                Start a conversation
                            </h2>
                            <p className="text-slate-400">
                                {hasDocuments
                                    ? 'Ask questions about your uploaded documents and get grounded answers with source citations.'
                                    : 'Upload some documents first to start asking questions.'}
                            </p>
                        </div>
                    </div>
                ) : (
                    <>
                        {messages.map(message => (
                            <Message key={message.id} message={message} isUser={message.isUser} />
                        ))}
                        {isLoading && (
                            <div className="flex justify-start mb-4">
                                <div className="flex items-center gap-3">
                                    <div className="p-2 bg-slate-700 rounded-full">
                                        <Loader2 className="w-4 h-4 text-primary-400 animate-spin" />
                                    </div>
                                    <div className="chat-bubble chat-bubble-assistant">
                                        <div className="flex gap-1">
                                            <span className="w-2 h-2 bg-slate-500 rounded-full animate-pulse" style={{ animationDelay: '0ms' }} />
                                            <span className="w-2 h-2 bg-slate-500 rounded-full animate-pulse" style={{ animationDelay: '150ms' }} />
                                            <span className="w-2 h-2 bg-slate-500 rounded-full animate-pulse" style={{ animationDelay: '300ms' }} />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </>
                )}
            </div>

            {/* Input */}
            <div className="border-t border-slate-800 bg-slate-900/50 backdrop-blur-sm p-4">
                <div className="max-w-4xl mx-auto">
                    {!hasDocuments && (
                        <div className="mb-3 px-4 py-2 bg-amber-600/10 border border-amber-600/20 rounded-lg text-sm text-amber-400">
                            ⚠️ No documents indexed. Upload documents to enable chat.
                        </div>
                    )}

                    <div className="flex gap-3">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={handleKeyPress}
                            placeholder={hasDocuments ? "Ask a question..." : "Upload documents first..."}
                            disabled={!hasDocuments || isLoading}
                            className="input flex-1"
                        />
                        <button
                            onClick={handleSend}
                            disabled={!input.trim() || !hasDocuments || isLoading}
                            className="btn btn-primary flex items-center gap-2 px-6"
                        >
                            {isLoading ? (
                                <Loader2 className="w-4 h-4 animate-spin" />
                            ) : (
                                <Send className="w-4 h-4" />
                            )}
                            Send
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
