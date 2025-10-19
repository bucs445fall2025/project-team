"use client"
import { useState } from 'react';
import { TrendingUp, Eye, EyeOff, Check, X } from 'lucide-react';
import Logo from '@/components/logo';

export default function SignUp() {
	const [firstName, setFirstName] = useState('');
	const [lastName, setLastName] = useState('');
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');
	const [retypePassword, setRetypePassword] = useState('');
	const [showPassword, setShowPassword] = useState(false);
	const [showRetypePassword, setShowRetypePassword] = useState(false);
	const [agreeTerms, setAgreeTerms] = useState(false);
	const [newsletter, setNewsletter] = useState(false);
	const [isLoading, setIsLoading] = useState(false);

	const passwordRequirements = {
		length: password.length >= 8,
		number: /\d/.test(password),
		symbol: /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password),
		capital: /[A-Z]/.test(password),
	};

	const allRequirementsMet = Object.values(passwordRequirements).every(Boolean);
	const passwordsMatch = password === retypePassword && password.length > 0;
	const isFormValid = firstName && lastName && email && allRequirementsMet && passwordsMatch && agreeTerms;

	const getPasswordStrength = () => {
		const metRequirements = Object.values(passwordRequirements).filter(Boolean).length;
		if (metRequirements === 0) return { strength: 0, label: '', color: 'bg-gray-400' };
		if (metRequirements <= 1) return { strength: 25, label: 'Weak', color: 'bg-red-500' };
		if (metRequirements <= 2) return { strength: 50, label: 'Fair', color: 'bg-orange-500' };
		if (metRequirements <= 3) return { strength: 75, label: 'Good', color: 'bg-yellow-500' };
		return { strength: 100, label: 'Strong', color: 'bg-green-500' };
	};

	const { strength, label, color } = getPasswordStrength();

	const handleSignUp = () => {
		setIsLoading(true);
		console.log('Sign up attempt:', {
			firstName,
			lastName,
			email,
			password,
			agreeTerms,
			newsletter,
		});
		setTimeout(() => setIsLoading(false), 1000);
	};

	const handleLogin = () => {
		window.location.href = '/login';
	};

	const RequirementItem = ({ met, text }: any) => (
		<div className="flex items-center space-x-2">
			{met ? (
				<Check className="w-4 h-4 text-green-400" />
			) : (
				<X className="w-4 h-4 text-gray-500" />
			)}
			<span className={met ? 'text-green-400 text-sm' : 'text-gray-400 text-sm'}>
				{text}
			</span>
		</div>
	);

	return (
		<div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center px-4 py-8">
			{/* Background elements */}
			<div className="absolute top-0 left-0 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
			<div className="absolute bottom-0 right-0 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl"></div>

			{/* Sign Up Card */}
			<div className="w-full max-w-md relative z-10">
				<div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-8 shadow-2xl">
					{/* Logo */}
					<Logo />

					{/* Heading */}
					<div className="text-center mb-8">
						<h1 className="text-3xl font-bold text-white mb-2">Create Account</h1>
						<p className="text-gray-400">Join thousands of smart investors</p>
					</div>

					{/* Form */}
					<div className="space-y-4">
						{/* First Name */}
						<div>
							<label className="block text-sm font-medium text-gray-300 mb-2">
								First Name
							</label>
							<input
								type="text"
								placeholder="John"
								value={firstName}
								onChange={(e) => setFirstName(e.target.value)}
								className="w-full px-4 py-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
							/>
						</div>

						{/* Last Name */}
						<div>
							<label className="block text-sm font-medium text-gray-300 mb-2">
								Last Name
							</label>
							<input
								type="text"
								placeholder="Doe"
								value={lastName}
								onChange={(e) => setLastName(e.target.value)}
								className="w-full px-4 py-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
							/>
						</div>

						{/* Email */}
						<div>
							<label className="block text-sm font-medium text-gray-300 mb-2">
								Email
							</label>
							<input
								type="email"
								placeholder="john@example.com"
								value={email}
								onChange={(e) => setEmail(e.target.value)}
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
									placeholder="Create a strong password"
									value={password}
									onChange={(e) => setPassword(e.target.value)}
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

							{/* Password Strength Meter */}
							{password && (
								<div className="mt-3 space-y-2">
									<div className="flex items-center justify-between">
										<span className="text-xs text-gray-400">Strength</span>
										{label && <span className={`text-xs font-semibold ${color.replace('bg-', 'text-')}`}>{label}</span>}
									</div>
									<div className="w-full h-2 bg-white/10 rounded-full overflow-hidden">
										<div
											className={`h-full ${color} transition-all duration-300`}
											style={{ width: `${strength}%` }}
										></div>
									</div>
								</div>
							)}

							{/* Password Requirements */}
							{password && (
								<div className="mt-3 p-3 bg-white/5 border border-white/10 rounded-lg space-y-2">
									<RequirementItem met={passwordRequirements.length} text="At least 8 characters" />
									<RequirementItem met={passwordRequirements.capital} text="One capital letter" />
									<RequirementItem met={passwordRequirements.number} text="One number" />
									<RequirementItem met={passwordRequirements.symbol} text="One symbol (!@#$%^&*)" />
								</div>
							)}
						</div>

						{/* Retype Password */}
						<div>
							<label className="block text-sm font-medium text-gray-300 mb-2">
								Confirm Password
							</label>
							<div className="relative">
								<input
									type={showRetypePassword ? 'text' : 'password'}
									placeholder="Retype your password"
									value={retypePassword}
									onChange={(e) => setRetypePassword(e.target.value)}
									className={`w-full px-4 py-3 rounded-lg bg-white/10 border transition pr-12 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:border-transparent ${retypePassword
											? passwordsMatch
												? 'border-green-500/50 focus:ring-green-500'
												: 'border-red-500/50 focus:ring-red-500'
											: 'border-white/20 focus:ring-blue-500'
										}`}
								/>
								<button
									type="button"
									onClick={() => setShowRetypePassword(!showRetypePassword)}
									className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-300 transition"
								>
									{showRetypePassword ? (
										<EyeOff className="w-5 h-5" />
									) : (
										<Eye className="w-5 h-5" />
									)}
								</button>
							</div>
							{retypePassword && !passwordsMatch && (
								<p className="text-red-400 text-sm mt-1">Passwords do not match</p>
							)}
						</div>

						{/* Checkboxes */}
						<div className="space-y-3 pt-4">
							{/* Terms and Services */}
							<label className="flex items-start space-x-3 cursor-pointer">
								<input
									type="checkbox"
									checked={agreeTerms}
									onChange={(e) => setAgreeTerms(e.target.checked)}
									className="mt-1 w-4 h-4 rounded bg-white/10 border border-white/20 text-blue-600 focus:ring-2 focus:ring-blue-500 cursor-pointer"
								/>
								<span className="text-sm text-gray-400">
									I agree to the{' '}
									<a href="#" className="text-blue-400 hover:text-blue-300 transition">
										Terms and Services
									</a>{' '}
									and{' '}
									<a href="#" className="text-blue-400 hover:text-blue-300 transition">
										Privacy Policy
									</a>
									<span className="text-red-400">*</span>
								</span>
							</label>

							{/* Newsletter */}
							<label className="flex items-start space-x-3 cursor-pointer">
								<input
									type="checkbox"
									checked={newsletter}
									onChange={(e) => setNewsletter(e.target.checked)}
									className="mt-1 w-4 h-4 rounded bg-white/10 border border-white/20 text-blue-600 focus:ring-2 focus:ring-blue-500 cursor-pointer"
								/>
								<span className="text-sm text-gray-400">
									Send me emails about stock tips, analysis, and market updates
								</span>
							</label>
						</div>

						{/* Sign Up Button */}
						<button
							onClick={handleSignUp}
							disabled={!isFormValid || isLoading}
							className="w-full py-3 px-4 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 disabled:from-gray-600 disabled:to-gray-600 text-white font-semibold rounded-lg transition disabled:cursor-not-allowed mt-6"
						>
							{isLoading ? 'Creating Account...' : 'Create Account'}
						</button>
					</div>

					{/* Divider */}
					<div className="my-6 flex items-center">
						<div className="flex-1 h-px bg-white/10"></div>
						<span className="px-3 text-xs text-gray-500">OR</span>
						<div className="flex-1 h-px bg-white/10"></div>
					</div>

					{/* Login Link */}
					<div className="text-center">
						<p className="text-gray-400 text-sm">
							Already have an account?{' '}
							<button
								onClick={handleLogin}
								className="text-blue-400 hover:text-blue-300 font-semibold transition"
							>
								Sign In
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