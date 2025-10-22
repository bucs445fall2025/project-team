"use client"
import { useState } from 'react';
import { TrendingUp, Eye, EyeOff } from 'lucide-react';
import Logo from '@/components/logo';

export default function Login() {
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
	const [showPassword, setShowPassword] = useState(false);
	const [isLoading, setIsLoading] = useState(false);

	const handleLogin = () => {
		setIsLoading(true);
		// TODO: Add api endpoint to login on server
		console.log('Login attempt:', { username, password });
		setTimeout(() => setIsLoading(false), 1000);
	};

	const handleSignUp = () => {
		window.location.href = '/signup';
	};

	const handleForgotPassword = () => {
		console.log('Forgot password clicked');
	};

	return (
		<div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center px-4">
			{/* Background elements */}
			<div className="absolute top-0 left-0 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
			<div className="absolute bottom-0 right-0 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl"></div>

			{/* Login Card */}
			<div className="w-full max-w-md relative z-10">
				<div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-8 shadow-2xl">
					{/* Logo */}
					<Logo />

					{/* Heading */}
					<div className="text-center mb-8">
						<h1 className="text-3xl font-bold text-white mb-2">Welcome Back</h1>
						<p className="text-gray-400">Sign in to your account to continue</p>
					</div>

					{/* Form */}
					<div className="space-y-5">
						{/* Username */}
						<div>
							<label className="block text-sm font-medium text-gray-300 mb-2">
								Username or Email
							</label>
							<input
								type="text"
								placeholder="Enter your username or email"
								value={username}
								onChange={(e) => setUsername(e.target.value)}
								onKeyPress={(e) => e.key === 'Enter' && handleLogin()}
								className="w-full px-4 py-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
							/>
						</div>

						{/* Password */}
						<div>
							<label className="block text-sm font-medium text-gray-300 mb-2">
								Password
							</label>
							<div className="relative">
								<input
									type={showPassword ? 'text' : 'password'}
									placeholder="Enter your password"
									value={password}
									onChange={(e) => setPassword(e.target.value)}
									onKeyPress={(e) => e.key === 'Enter' && handleLogin()}
									className="w-full px-4 py-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition pr-12"
								/>
								<button
									type="button"
									onClick={() => setShowPassword(!showPassword)}
									className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-300 transition"
								>
									{showPassword ? (
										<EyeOff className="w-5 h-5" />
									) : (
										<Eye className="w-5 h-5" />
									)}
								</button>
							</div>
						</div>

						{/* Forgot Password Link */}
						<div className="text-right">
							<button
								onClick={handleForgotPassword}
								className="text-sm text-blue-400 hover:text-blue-300 transition"
							>
								Forgot Password?
							</button>
						</div>

						{/* Login Button */}
						<button
							onClick={handleLogin}
							disabled={isLoading || !username || !password}
							className="w-full py-3 px-4 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 disabled:from-gray-600 disabled:to-gray-600 text-white font-semibold rounded-lg transition disabled:cursor-not-allowed"
						>
							{isLoading ? 'Signing in...' : 'Sign In'}
						</button>
					</div>

					{/* Divider */}
					<div className="my-6 flex items-center">
						<div className="flex-1 h-px bg-white/10"></div>
						<span className="px-3 text-xs text-gray-500">OR</span>
						<div className="flex-1 h-px bg-white/10"></div>
					</div>

					{/* Sign Up Link */}
					<div className="text-center">
						<p className="text-gray-400 text-sm">
							Don't have an account?{' '}
							<button
								onClick={handleSignUp}
								className="text-blue-400 hover:text-blue-300 font-semibold transition"
							>
								Create Account
							</button>
						</p>
					</div>
				</div>

				{/* Footer text */}
				<div className="text-center mt-6 text-xs text-gray-500">
					<p>© 2025 StockIQ. All rights reserved.</p>
				</div>
			</div>
		</div>
	);
}