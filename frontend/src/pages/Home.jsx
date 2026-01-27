import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { TrendingUp, ArrowRight, Shield, Zap, Globe, MessageSquare, BarChart3, Newspaper } from 'lucide-react';
import ThemeToggle from '../components/ThemeToggle';


const Home = () => {
    const navigate = useNavigate();

    return (
        <div className="min-h-screen bg-slate-50 dark:bg-[#0a0c10] text-slate-900 dark:text-white transition-colors duration-300 relative overflow-hidden">
            {/* Background Glows */}
            <div className="absolute top-0 left-0 w-[600px] h-[600px] bg-blue-600/10 dark:bg-blue-600/20 rounded-full blur-[120px] pointer-events-none" />
            <div className="absolute bottom-0 right-0 w-[600px] h-[600px] bg-purple-600/10 dark:bg-purple-600/20 rounded-full blur-[120px] pointer-events-none" />

            {/* Navbar */}
            <nav className="relative z-50 container mx-auto px-6 py-6 flex justify-between items-center">
                <div className="flex items-center gap-3 group cursor-pointer" onClick={() => navigate('/')}>
                    <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/20 group-hover:scale-110 transition-transform">
                        <TrendingUp className="w-6 h-6 text-white" />
                    </div>
                    <span className="text-xl font-black tracking-tighter uppercase">MarketPulse <span className="text-blue-600">AI</span></span>
                </div>

                <div className="flex items-center gap-6">
                    <ThemeToggle />
                    <Link to="/login" className="hidden md:block font-bold text-sm hover:text-blue-600 transition-colors uppercase tracking-widest">Login</Link>
                    <Link to="/signup" className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-bold text-sm shadow-xl shadow-blue-500/20 transition-all active:scale-95 uppercase tracking-widest">Sign Up</Link>
                </div>
            </nav>

            {/* Hero Section */}
            <main className="relative z-10 w-full mx-auto px-6 pt-16 pb-20 md:pt-24 md:pb-32">
                <div className="w-full max-w-5xl mx-auto text-center">
                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-500/10 text-blue-600 dark:text-blue-400 text-[10px] font-black uppercase tracking-[0.2em] mb-8 animate-in fade-in slide-in-from-bottom-2 duration-500">
                        <span className="relative flex h-2 w-2">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                            <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
                        </span>
                        Next generation market intelligence
                    </div>

                    <h1 className="text-5xl md:text-8xl font-black tracking-tight mb-8 leading-[0.9] animate-in fade-in slide-in-from-bottom-4 duration-700">
                        Master the Market with <span className="bg-gradient-to-r from-blue-600 to-indigo-500 bg-clip-text text-transparent">Precision AI</span>
                    </h1>

                    <p className="text-lg md:text-xl text-slate-500 dark:text-gray-400 mb-12 max-w-2xl mx-auto leading-relaxed animate-in fade-in slide-in-from-bottom-6 duration-1000">
                        Real-time sentiment analysis, global indices tracking, and AI-powered insights for the modern trader. Stop guessing, start deciding.
                    </p>

                    <div className="flex flex-col sm:flex-row items-center justify-center gap-4 animate-in fade-in slide-in-from-bottom-8 duration-1000">
                        <button
                            onClick={() => navigate('/signup')}
                            className="w-full sm:w-auto px-10 py-5 bg-blue-600 hover:bg-blue-700 text-white rounded-2xl font-black shadow-2xl shadow-blue-500/40 transition-all active:scale-[0.98] flex items-center justify-center gap-3 group"
                        >
                            Get Started Free
                            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                        </button>
                        <button
                            onClick={() => navigate('/login')}
                            className="w-full sm:w-auto px-10 py-5 bg-white dark:bg-white/5 border border-slate-200 dark:border-white/10 rounded-2xl font-black hover:bg-slate-50 dark:hover:bg-white/10 transition-all active:scale-[0.98]"
                        >
                            View Dashboard
                        </button>
                    </div>
                </div>

                {/* Features Preview */}
                <div className="mt-20 md:mt-32 grid grid-cols-1 md:grid-cols-3 gap-8">
                    {[
                        {
                            icon: <Zap className="w-6 h-6 text-amber-500" />,
                            title: "Real-time Ticker",
                            desc: "Streaming global commodities and indices with millisecond precision."
                        },
                        {
                            icon: <Shield className="w-6 h-6 text-emerald-500" />,
                            title: "Sentiment Analysis",
                            desc: "Deep-learning models analyze news headlines to gauge market mood."
                        },
                        {
                            icon: <MessageSquare className="w-6 h-6 text-blue-500" />,
                            title: "AI Assistant",
                            desc: "Direct access to market experts powered by Gemini 2.5."
                        }
                    ].map((feature, i) => (
                        <div key={i} className="bg-white/40 dark:bg-gray-900/40 backdrop-blur-xl border border-slate-200 dark:border-white/10 p-8 rounded-3xl hover:border-blue-500/30 transition-all group">
                            <div className="w-12 h-12 bg-slate-100 dark:bg-white/5 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                                {feature.icon}
                            </div>
                            <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
                            <p className="text-sm text-slate-500 dark:text-gray-400 leading-relaxed">{feature.desc}</p>
                        </div>
                    ))}
                </div>
            </main>

            {/* Footer Decoration */}
            <div className="absolute bottom-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-blue-500/20 to-transparent"></div>

        </div>
    );
};

export default Home;
