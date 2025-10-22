import {TrendingUp } from 'lucide-react'

export default function Logo() {
	return (
		<div className="flex justify-center mb-8">
			<div className="flex items-center space-x-2">
				<div className="w-12 h-12 bg-gradient-to-br from-blue-400 to-cyan-400 rounded-lg flex items-center justify-center">
					<TrendingUp className="w-8 h-8 text-blue-900" />
				</div>
				<span className="text-2xl font-bold text-white">StockIQ</span>
			</div>
		</div>
	)
} 