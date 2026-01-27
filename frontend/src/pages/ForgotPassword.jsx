import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Mail, ArrowLeft, TrendingUp, CheckCircle, Home } from 'lucide-react';
import ThemeToggle from '../components/ThemeToggle';

const ForgotPassword = () => {
    const [email, setEmail] = useState('');
    const [isSubmitted, setIsSubmitted] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault();
        // Mock forgot password logic
        console.log('Reset link requested for:', email);
        setIsSubmitted(true);
    };

    return (
        <div className="min-h-screen bg-slate-50 dark:bg-[#0a0c10] flex flex-col transition-colors duration-300 relative overflow-hidden">
            {/* Background Glows */}
            <div className="absolute top-0 left-0 w-[500px] h-[500px] bg-blue-600/5 dark:bg-blue-600/10 rounded-full blur-[120px] pointer-events-none" />
            <div className="absolute bottom-0 right-0 w-[500px] h-[500px] bg-purple-600/5 dark:bg-purple-600/10 rounded-full blur-[120px] pointer-events-none" />

            <div className="absolute top-6 right-6 z-50 flex items-center gap-3">
                <Link
                    to="/"
                    className="p-2.5 rounded-xl bg-slate-200 dark:bg-white/5 text-slate-600 dark:text-gray-400 hover:bg-blue-500/10 hover:text-blue-500 transition-all border border-slate-300 dark:border-white/10"
                    title="Back to Home"
                >
                    <Home className="w-5 h-5" />
                </Link>
                <ThemeToggle />
            </div>

            <div className="flex-1 flex flex-col justify-center items-center p-6 relative z-10">
                <div className="w-full max-w-md bg-white dark:bg-gray-900/40 backdrop-blur-xl border border-slate-200 dark:border-white/10 rounded-3xl p-8 shadow-2xl transition-all">
                    <div className="flex flex-col items-center mb-10">
                        <div className="w-16 h-16 bg-blue-600 rounded-2xl flex items-center justify-center mb-6 shadow-xl shadow-blue-500/20">
                            <TrendingUp className="w-8 h-8 text-white" />
                        </div>
                        <h1 className="text-3xl font-black text-slate-900 dark:text-white mb-2">Reset Password</h1>
                        <p className="text-slate-500 dark:text-gray-400 text-sm">We'll send a link to your email</p>
                    </div>

                    {!isSubmitted ? (
                        <form onSubmit={handleSubmit} className="space-y-6">
                            <div className="space-y-2">
                                <label className="text-xs font-bold text-slate-700 dark:text-gray-400 uppercase tracking-widest ml-1">Email Address</label>
                                <div className="relative group">
                                    <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                        <Mail className="h-5 w-5 text-slate-400 group-focus-within:text-blue-500 transition-colors" />
                                    </div>
                                    <input
                                        type="email"
                                        required
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        className="block w-full pl-11 pr-4 py-3.5 bg-slate-100 dark:bg-black/20 border border-slate-200 dark:border-white/5 rounded-2xl text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all transition-all"
                                        placeholder="name@example.com"
                                    />
                                </div>
                            </div>

                            <button
                                type="submit"
                                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 rounded-2xl shadow-xl shadow-blue-500/20 transition-all active:scale-[0.98] flex items-center justify-center gap-2 group"
                            >
                                Send Reset Link
                            </button>
                        </form>
                    ) : (
                        <div className="text-center animate-in zoom-in-95 duration-300">
                            <div className="flex justify-center mb-6">
                                <CheckCircle className="w-16 h-16 text-emerald-500" />
                            </div>
                            <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-2">Link Sent!</h2>
                            <p className="text-slate-500 dark:text-gray-400 text-sm mb-8">
                                If an account exists with that email, we've sent instructions to reset your password.
                            </p>
                            <button
                                onClick={() => setIsSubmitted(false)}
                                className="text-sm font-bold text-blue-600 hover:text-blue-500 transition-colors"
                                title="Try another email"
                            >
                                Try another email
                            </button>
                        </div>
                    )}

                    <div className="mt-8 text-center">
                        <Link to="/login" title="Back to Sign In" className="inline-flex items-center gap-2 text-sm font-bold text-slate-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-white transition-colors">
                            <ArrowLeft className="w-4 h-4" />
                            Back to Sign In
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ForgotPassword;
