"use client"
import { useState, useEffect } from 'react'
import { TrendingUp } from 'lucide-react'
import SearchBar from '@/components/home_page/search-bar'
import MarketOverview from '@/components/home_page/market-overview'
import MarketNews from '@/components/home_page/market-news'
import Watchlist from '@/components/home_page/watchlist'

export default function Header() {
	return (
		<div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 ">
			<div className="flex flex-col gap-6 p-4 md:p-6">
				<div className="flex justify-center">
					<SearchBar />
				</div>
				<div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
					<MarketOverview />
				</div>
				<div className="grid gap-4 md:grid-cols-3">
					<div className="md:col-span-2">
						<MarketNews />
					</div>
					<div>
						<Watchlist />
					</div>
				</div>
			</div>
		</div>
	)
}