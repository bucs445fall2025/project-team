"use client";
import { useState } from 'react';
import { TrendingUp, BarChart3, Search, Shield, Zap, Bell } from 'lucide-react';

export default function StockAnalysisLanding() {
	const [email, setEmail] = useState('');
	const [ticker, setTicker] = useState('');

	const handleEmailSubmit = () => {
		console.log('Email submitted:', email);
	};

	const handleSearch = () => {
		console.log('Searching for:', ticker);
	};

	return (
		<div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
			<nav className="border-b border-white/10 bg-slate-900/50 backdrop-blur-sm">
				<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
					<div className="flex justify-between items-center h-16">
						<div className="flex items-center space-x-2">
							<TrendingUp className="w-8 h-8 text-blue-400" />
							<span className="text-xl font-bold text-white">StockIQ</span>
						</div>
						<div className="hidden md:flex space-x-8">
							<a href="#features" className="text-gray-300 hover:text-white transition">Features</a>
							<a href="#pricing" className="text-gray-300 hover:text-white transition">Pricing</a>
							<a href="#about" className="text-gray-300 hover:text-white transition">About</a>
						</div>
						<button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition">
							Sign In
						</button>
					</div>
				</div>
			</nav>

			<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
				<div className="text-center">
					<h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
						:smiley_face: Analysis
						<span className="block text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400">
							Using the best AI known to man
						</span>
					</h1>
					<p className="text-xl text-gray-300 mb-12 max-w-2xl mx-auto">
						Make informed investment decisions with real-time data, advanced analytics, and AI-powered insights.
					</p>

					<div className="max-w-2xl mx-auto mb-8">
						<div className="flex gap-2">
							<div className="flex-1 relative">
								<Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
								<input
									type="text"
									placeholder="Enter stock ticker (e.g., AAPL, TSLA, GOOGL)"
									value={ticker}
									onChange={(e) => setTicker(e.target.value)}
									onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
									className="w-full pl-12 pr-4 py-4 rounded-xl bg-white/10 border border-white/20 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 backdrop-blur-sm"
								/>
							</div>
							<button
								onClick={handleSearch}
								className="px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl transition"
							>
								Analyze
							</button>
						</div>
					</div>

					<div className="grid grid-cols-3 gap-8 max-w-3xl mx-auto mt-16">
						<div>
							<div className="text-3xl font-bold text-blue-400">10K+</div>
							<div className="text-gray-400 mt-1">Active Users</div>
						</div>
						<div>
							<div className="text-3xl font-bold text-blue-400">500M+</div>
							<div className="text-gray-400 mt-1">Data Points</div>
						</div>
						<div>
							<div className="text-3xl font-bold text-blue-400">99.9%</div>
							<div className="text-gray-400 mt-1">Uptime</div>
						</div>
					</div>
				</div>
			</div>

			<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
				<div className="text-center mb-16">
					<h2 className="text-4xl font-bold text-white mb-4">Powerful Features</h2>
					<p className="text-gray-400 text-lg">Everything you need to analyze stocks like a pro</p>
				</div>

				<div className="grid md:grid-cols-3 gap-8">
					<div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:bg-white/10 transition">
						<div className="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center mb-4">
							<BarChart3 className="w-6 h-6 text-blue-400" />
						</div>
						<h3 className="text-xl font-semibold text-white mb-3">Advanced Charts</h3>
						<p className="text-gray-400">
							Interactive charts with technical indicators, patterns, and real-time updates.
						</p>
					</div>

					<div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:bg-white/10 transition">
						<div className="w-12 h-12 bg-cyan-500/20 rounded-lg flex items-center justify-center mb-4">
							<Zap className="w-6 h-6 text-cyan-400" />
						</div>
						<h3 className="text-xl font-semibold text-white mb-3">AI Insights</h3>
						<p className="text-gray-400">
							Get AI-powered predictions and sentiment analysis from market data.
						</p>
					</div>

					<div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:bg-white/10 transition">
						<div className="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center mb-4">
							<Bell className="w-6 h-6 text-purple-400" />
						</div>
						<h3 className="text-xl font-semibold text-white mb-3">Smart Alerts</h3>
						<p className="text-gray-400">
							Set custom alerts for price movements, volume changes, and news events.
						</p>
					</div>

					<div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:bg-white/10 transition">
						<div className="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center mb-4">
							<Shield className="w-6 h-6 text-green-400" />
						</div>
						<h3 className="text-xl font-semibold text-white mb-3">Portfolio Tracking</h3>
						<p className="text-gray-400">
							Monitor your investments and analyze portfolio performance in real-time.
						</p>
					</div>

					<div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:bg-white/10 transition">
						<div className="w-12 h-12 bg-orange-500/20 rounded-lg flex items-center justify-center mb-4">
							<TrendingUp className="w-6 h-6 text-orange-400" />
						</div>
						<h3 className="text-xl font-semibold text-white mb-3">Fundamental Data</h3>
						<p className="text-gray-400">
							Access comprehensive financial statements, ratios, and company metrics.
						</p>
					</div>

					<div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:bg-white/10 transition">
						<div className="w-12 h-12 bg-pink-500/20 rounded-lg flex items-center justify-center mb-4">
							<Search className="w-6 h-6 text-pink-400" />
						</div>
						<h3 className="text-xl font-semibold text-white mb-3">Stock Screener</h3>
						<p className="text-gray-400">
							Filter thousands of stocks based on your custom criteria and strategies.
						</p>
					</div>
				</div>
			</div>

			<div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
				<div className="bg-gradient-to-r from-blue-600 to-cyan-600 rounded-3xl p-12 text-center">
					<h2 className="text-4xl font-bold text-white mb-4">
						Start Analyzing Stocks Today
					</h2>
					<p className="text-blue-100 text-lg mb-8">
						Join thousands of investors making smarter decisions with our platform
					</p>
					<div className="max-w-md mx-auto flex gap-2">
						<input
							type="email"
							placeholder="Enter your email"
							value={email}
							onChange={(e) => setEmail(e.target.value)}
							onKeyPress={(e) => e.key === 'Enter' && handleEmailSubmit()}
							className="flex-1 px-6 py-4 rounded-xl bg-white text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-white"
						/>
						<button
							onClick={handleEmailSubmit}
							className="px-8 py-4 bg-slate-900 hover:bg-slate-800 text-white font-semibold rounded-xl transition"
						>
							Get Started
						</button>
					</div>
				</div>
			</div>

			<footer className="border-t border-white/10 bg-slate-900/50">
				<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
					<div className="grid md:grid-cols-4 gap-8">
						<div>
							<div className="flex items-center space-x-2 mb-4">
								<TrendingUp className="w-6 h-6 text-blue-400" />
								<span className="text-lg font-bold text-white">StockIQ</span>
							</div>
							<p className="text-gray-400 text-sm">
								Professional stock analysis tools for modern investors.
							</p>
						</div>
						<div>
							<h4 className="text-white font-semibold mb-4">Product</h4>
							<ul className="space-y-2 text-gray-400 text-sm">
								<li><a href="#" className="hover:text-white transition">Features</a></li>
								<li><a href="#" className="hover:text-white transition">Pricing</a></li>
								<li><a href="#" className="hover:text-white transition">API</a></li>
							</ul>
						</div>
						<div>
							<h4 className="text-white font-semibold mb-4">Company</h4>
							<ul className="space-y-2 text-gray-400 text-sm">
								<li><a href="#" className="hover:text-white transition">About</a></li>
								<li><a href="#" className="hover:text-white transition">Blog</a></li>
								<li><a href="#" className="hover:text-white transition">Careers</a></li>
							</ul>
						</div>
						<div>
							<h4 className="text-white font-semibold mb-4">Legal</h4>
							<ul className="space-y-2 text-gray-400 text-sm">
								<li><a href="#" className="hover:text-white transition">Privacy</a></li>
								<li><a href="#" className="hover:text-white transition">Terms</a></li>
								<li><a href="#" className="hover:text-white transition">Security</a></li>
							</ul>
						</div>
					</div>
					<div className="border-t border-white/10 mt-8 pt-8 text-center text-gray-400 text-sm">
						© 2025 smiley-face. All rights reserved.
					</div>
				</div>
			</footer>
		</div>
	);
}