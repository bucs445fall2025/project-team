"use client"
import { TrendingUp, ArrowLeft } from 'lucide-react';
import Logo from '@/components/logo';

export default function TermsOfService() {
	return (
		<div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 px-4 py-8">
			<div className="absolute top-0 left-0 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
			<div className="absolute bottom-0 right-0 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl"></div>

			<div className="max-w-4xl mx-auto relative z-10">
				<div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-8 shadow-2xl">
					<Logo />

					<button
						onClick={() => window.history.back()}
						className="flex items-center space-x-2 text-blue-400 hover:text-blue-300 transition mb-6"
					>
						<ArrowLeft className="w-4 h-4" />
						<span>Back</span>
					</button>

					<h1 className="text-4xl font-bold text-white mb-2 text-center">Terms of Service</h1>
					<p className="text-gray-400 text-center mb-8">Last Updated: Right Now (we're totally updating this every second)</p>

					<div className="space-y-6 text-gray-300">
						<section>
							<h2 className="text-2xl font-bold text-white mb-3">1. Acceptance of Terms</h2>
							<p>
								By using StockIQ, you agree to pretend you read this entire document. We both know you didn't,
								but let's maintain the illusion. If you disagree with these terms, please close this tab and go
								touch some grass (not financial advice).
							</p>
						</section>

						<section>
							<h2 className="text-2xl font-bold text-white mb-3">2. Investment Disclaimer</h2>
							<p className="mb-2">
								StockIQ does NOT provide financial advice. Seriously. We're a school project made by students
								who eat ramen for dinner and think "diversifying" means buying both regular AND spicy ramen.
							</p>
							<p>
								Any investment decisions you make based on our platform are 100% your responsibility. We will
								not be held liable when you lose your lunch money on a meme stock because our AI said "stonks only go up 🚀".
							</p>
						</section>

						<section>
							<h2 className="text-2xl font-bold text-white mb-3">3. User Conduct</h2>
							<p className="mb-2">You agree to NOT:</p>
							<ul className="list-disc list-inside space-y-1 ml-4">
								<li>Use our platform to orchestrate the next GameStop short squeeze</li>
								<li>Blame us when your portfolio looks like a ski slope going downhill</li>
								<li>Ask us "wen moon?" (we don't know, we're just trying to pass this class)</li>
								<li>Hack our database (it's not worth it, we literally have nothing of value)</li>
								<li>Spread FUD (Fear, Uncertainty, and Doubt) unless it's about our coding skills</li>
							</ul>
						</section>

						<section>
							<h2 className="text-2xl font-bold text-white mb-3">4. Account Security</h2>
							<p>
								Please don't use "password123" as your password. We beg you. Your account security is your
								responsibility. If someone guesses your password is "Bitcoin" and steals your account, that's
								on you, chief.
							</p>
						</section>

						<section>
							<h2 className="text-2xl font-bold text-white mb-3">5. Intellectual Property</h2>
							<p>
								All content on StockIQ belongs to us (the broke college students who made this). Please don't
								steal our mediocre code. If you want to use it, just ask nicely. We'll probably say yes because
								we're desperate for portfolio material.
							</p>
						</section>

						<section>
							<h2 className="text-2xl font-bold text-white mb-3">6. Service Availability</h2>
							<p>
								StockIQ may go down at any time because:
							</p>
							<ul className="list-disc list-inside space-y-1 ml-4 mt-2">
								<li>We forgot to pay the AWS bill (student budget, ya know)</li>
								<li>Someone spilled coffee on the server (it's a laptop under someone's bed)</li>
								<li>The semester ended and we all went home</li>
								<li>We're sleeping because we have a midterm tomorrow</li>
							</ul>
						</section>

						<section>
							<h2 className="text-2xl font-bold text-white mb-3">7. Limitation of Liability</h2>
							<p>
								In no event shall StockIQ be liable for any damages, including but not limited to: loss of
								profits, loss of savings, bad investment decisions, broken dreams of becoming a day trader,
								or the emotional damage from watching your stocks crash harder than our project presentation.
							</p>
						</section>

						<section>
							<h2 className="text-2xl font-bold text-white mb-3">8. Modifications to Service</h2>
							<p>
								We reserve the right to modify, suspend, or discontinue StockIQ at any time. Especially after
								we graduate and get real jobs. This is a school project, not a SaaS startup (yet... unless? 👀).
							</p>
						</section>

						<section>
							<h2 className="text-2xl font-bold text-white mb-3">9. Governing Law</h2>
							<p>
								These terms are governed by the laws of Common Sense and the Student Honor Code. Disputes will
								be resolved by rock-paper-scissors, best 2 out of 3.
							</p>
						</section>

						<section>
							<h2 className="text-2xl font-bold text-white mb-3">10. Contact Us</h2>
							<p>
								If you have questions about these Terms, please don't contact us during finals week. Any other
								time is fine. Slide into our DMs or carrier pigeon works too.
							</p>
						</section>

						<div className="bg-yellow-500/20 border border-yellow-500/50 rounded-lg p-4 mt-8">
							<p className="text-yellow-400 font-semibold">
								⚠️ FINAL REMINDER: This is a SCHOOL PROJECT. Do not make actual financial decisions based on
								this platform. We can barely decide what to eat for lunch, let alone manage your retirement fund.
							</p>
						</div>
					</div>

					<div className="text-center mt-8 text-xs text-gray-500">
						<p>© 2025 StockIQ. Built with caffeine and stress.</p>
					</div>
				</div>
			</div>
		</div>
	);
}