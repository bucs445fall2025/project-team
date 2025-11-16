"use client"
import { useState } from 'react';
import { TrendingUp, Eye, EyeOff, X } from 'lucide-react';
import Logo from '@/components/logo';

export default function Login() {
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');
	const [showPassword, setShowPassword] = useState(false);
	const [isLoading, setIsLoading] = useState(false);
	const [loginError, setLoginError] = useState(false);

	const handleLogin = async () => {
		setIsLoading(true);
		setLoginError(false);

		try {
			const response = await fetch('http://localhost:8000/api/auth/login', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					email: email,
					password: password,
				}),
			});

			if (response.status === 401) {
				setLoginError(true);
			} else if (response.ok) {
				const data = await response.json();

				document.cookie = `token=${data}; path=/; max-age=${60 * 60 * 24 * 7}`; // 7 days

				window.location.href = '/home';
			} else {
				setLoginError(true);
			}
		} catch (error) {
			console.error('Login error:', error);
			setLoginError(true);
		} finally {
			setIsLoading(false);
		}
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
						{/* Error Message */}
						{loginError && (
							<div className="flex items-center space-x-3 p-4 bg-red-500/20 border border-red-500/50 rounded-lg">
								<X className="w-5 h-5 text-red-400 flex-shrink-0" />
								<p className="text-red-400 text-sm font-medium">
									Email or password is incorrect
								</p>
							</div>
						)}

						{/* Email */}
						<div>
							<label className="block text-sm font-medium text-gray-300 mb-2">
								Email
							</label>
							<input
								type="email"
								placeholder="Enter your email"
								value={email}
								onChange={(e) => setEmail(e.target.value)}
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
							disabled={isLoading || !email || !password}
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