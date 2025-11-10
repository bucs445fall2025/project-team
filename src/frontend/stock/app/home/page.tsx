"use client"
import { useState, useEffect } from 'react'
import { TrendingUp } from 'lucide-react'
import SearchBar from '@/components/home_page/search-bar'
import MarketOverview from '@/components/home_page/market-overview'
import MarketNews from '@/components/home_page/market-news'
import Watchlist from '@/components/home_page/watchlist'

export default function Header() {
	const [firstName, setFirstName] = useState('')

	useEffect(() => {
		const fetchFirstName = async () => {
			try {
				
				// Get the token from cookies
				const token = document.cookie
					.split('; ')
					.find(row => row.startsWith('token='))
					?.split('=')[1]

				if (!token) {
					console.error('No token found')
					return
				}
				console.log("making to fetch")
				const response = await fetch('http://localhost:8000/api/auth/getFirstName', {
					method: 'GET',
					headers: {
						'Authorization': `Bearer ${token}`,
						'Content-Type': 'application/json',
					},
				})

				if (response.ok) {
					const data = await response.json()
					setFirstName(data || "Stranger")
				} else {
					console.error('Failed to fetch first name')
				}
			} catch (error) {
				console.error('Error fetching first name:', error)
			}
		}

		fetchFirstName()
	}, [])

	return (
		<div className="min-h-screen bg-black">
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