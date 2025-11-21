"use client"
import { TrendingUp, ArrowLeft, Shield } from 'lucide-react';
import Logo from '@/components/logo';

export default function PrivacyPolicy() {
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

					<div className="flex items-center justify-center space-x-3 mb-2">
						<Shield className="w-8 h-8 text-blue-400" />
						<h1 className="text-4xl font-bold text-white text-center">Privacy Policy</h1>
					</div>
					<p className="text-gray-400 text-center mb-8">Effective Date: When we remembered to write this</p>

					<div className="space-y-6 text-gray-300">
						<section>
							<h2 className="text-2xl font-bold text-white mb-3">Introduction</h2>
							<p>
								Welcome to the StockIQ Privacy Policy, aka "The Document Nobody Reads But Everyone Should."
								We're legally obligated to tell you what we do with your data, so...
							</p>
						</section>

						<section>
							<h2 className="text-2xl font-bold text-white mb-3">1. Information We Collect</h2>
							<p className="mb-2">When you use StockIQ, we collect:</p>
							<ul className="list-disc list-inside space-y-1 ml-4">
								<li>Your name (so we can pretend we know you)</li>
								<li>Your email (for spam... just kidding! For important updates only)</li>
								<li>Your password (encrypted so well even WE can't read it)</li>
								<li>Your terrible investment choices (no judgment... okay, maybe a little)</li>
							</ul>
						</section>

						<section>
							<h2 className="text-2xl font-bold text-white mb-3">2. How We Use Your Information</h2>
							<p className="mb-2">We use your data to:</p>
							<ul className="list-disc list-inside space-y-1 ml-4">
								<li>Make the app actually work (shocking, we know)</li>
								<li>Send you newsletters you signed up for (remember that checkbox you clicked?)</li>
								<li>Improve our algorithms that still can't beat Nancy Pelosi</li>
								<li>Debug crashes and fix bugs (there are many, send help)</li>
								<li>Generate statistics for our final project presentation</li>
								<li>Feel like real software engineers even though we're just students</li>
							</ul>
						</section>

						<section>
							<h2 className="text-2xl font-bold text-white mb-3">3. Information Sharing</h2>
							<p className="mb-2">
								We do NOT sell your data. Why? Because:
							</p>
							<ul className="list-disc list-inside space-y-1 ml-4">
								<li>Nobody wants to buy it (harsh but true)</li>
								<li>We're not evil corporations (yet)</li>
								<li>Our professor would fail us</li>
								<li>We actually respect your privacy (surprisingly)</li>
							</ul>
							<p className="mt-2">
								However, we may share your data with:
							</p>
							<ul className="list-disc list-inside space-y-1 ml-4 mt-1">
								<li>Our cloud hosting provider (they already have it anyway)</li>
								<li>Our professor for grading purposes (sorry)</li>
								<li>Law enforcement if they ask nicely with a warrant</li>
							</ul>
						</section>

						<section>
							<h2 className="text-2xl font-bold text-white mb-3">4. Data Security</h2>
							<p>
								We take security seriously! Your data is protected with industry-standard encryption, firewalls,
								and whatever other buzzwords we learned in our Cybersecurity class. Is it Fort Knox? No. Is it
								better than keeping your password on a sticky note? Absolutely.
							</p>
							<p className="mt-2">
								Our security measures include: bcrypt password hashing, HTTPS everywhere, regular security updates
								(when we remember), and praying nothing gets hacked before the semester ends.
							</p>
						</section>

						<section>
							<h2 className="text-2xl font-bold text-white mb-3">5. Your Rights</h2>
							<p className="mb-2">You have the right to:</p>
							<ul className="list-disc list-inside space-y-1 ml-4">
								<li>Access your data (just log in, it's right there)</li>
								<li>Delete your account (we'll miss you but we get it)</li>
								<li>Update your information (please fix those typos)</li>
								<li>Opt out of emails (but you'll miss our witty subject lines)</li>
								<li>Ask us what data we have on you (spoiler: not much)</li>
								<li>Complain if we mess up (constructive feedback appreciated)</li>
							</ul>
						</section>

						<section>
							<h2 className="text-2xl font-bold text-white mb-3">6. Cookies Policy</h2>
							<p>
								We use cookies to remember you're logged in. That's it. No tracking across the internet, no
								creepy ad targeting, just basic functionality. If you disable cookies, the site won't work.
								Don't disable cookies.
							</p>
						</section>

						<section>
							<h2 className="text-2xl font-bold text-white mb-3">7. Third-Party Services</h2>
							<p>
								We use some third-party services like AWS (for hosting) and maybe some stock APIs (for data).
								They have their own privacy policies that are probably longer and more boring than ours.
								Read them if you're having trouble sleeping.
							</p>
						</section>

						<section>
							<h2 className="text-2xl font-bold text-white mb-3">8. Children's Privacy</h2>
							<p>
								This platform is not intended for children under 13. If you're under 13, please go play
								Minecraft or something. Seriously, go enjoy your childhood. The stock market will still be
								here when you grow up (probably more volatile, but still here).
							</p>
						</section>

						<section>
							<h2 className="text-2xl font-bold text-white mb-3">9. International Users</h2>
							<p>
								If you're accessing this from outside the US, welcome! Your data might cross international
								borders because cloud servers are everywhere. We're not doing anything sketchy, it's just
								how the internet works.
							</p>
						</section>

						<section>
							<h2 className="text-2xl font-bold text-white mb-3">10. Changes to This Policy</h2>
							<p>
								We may update this policy when we learn new legal words or our professor tells us we forgot
								something important. We'll update the "Effective Date" at the top. Will you notice? Probably
								not. Will we send you an email? Maybe, if we remember.
							</p>
						</section>

						<section>
							<h2 className="text-2xl font-bold text-white mb-3">11. Data Retention</h2>
							<p>
								We'll keep your data as long as your account is active, or until we need to free up server
								space, or until we graduate and forget to renew the domain name. Whichever comes first.
							</p>
						</section>

						<section>
							<h2 className="text-2xl font-bold text-white mb-3">12. Contact Us</h2>
							<p>
								Questions about privacy? Concerns about your data? Want to know why we wrote this policy like
								a comedy routine? Feel free to reach out! We actually read our messages (unlike most companies).
							</p>
							<p className="mt-2">
								Best times to contact us: Not during midterms, not during finals, not at 3 AM (we're asleep),
								basically just weekday afternoons when we're procrastinating on other homework.
							</p>
						</section>

						<div className="bg-green-500/20 border border-green-500/50 rounded-lg p-4 mt-8">
							<p className="text-green-400 font-semibold">
								TL;DR: We collect basic info to make the site work, we don't sell your data (yet), we try our
								best to keep it secure, and you can delete your account anytime (coming soon). We're students, not
								evil tech giants (yet).
							</p>
						</div>
					</div>

					<div className="text-center mt-8 text-xs text-gray-500">
						<p>© 2025 StockIQ. Protecting your data better than we protect our GPA.</p>
					</div>
				</div>
			</div>
		</div>
	);
}