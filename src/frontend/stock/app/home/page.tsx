"use client"
import { useState, useEffect } from 'react'
import { TrendingUp } from 'lucide-react'

export default function HomePage() {
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
		<div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
			{/* Background elements */}
			<div className="fixed top-0 left-0 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl pointer-events-none"></div>
			<div className="fixed bottom-0 right-0 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>

			{/* Toolbar */}
			<div className="relative z-10 bg-white/5 backdrop-blur-xl border-b border-white/10">
				<div className="flex items-center justify-between px-6 py-4">
					{/* Logo */}
					<div className="flex items-center space-x-2">
						<div className="bg-gradient-to-br from-blue-500 to-cyan-500 p-2 rounded-lg">
							<TrendingUp className="w-6 h-6 text-white" />
						</div>
						<span className="text-2xl font-bold text-white">StockIQ</span>
					</div>

					{/* User Greeting */}
					<div className="text-white font-medium">
						{firstName ? `Hello ${firstName}` : 'Hello'}
					</div>
				</div>
			</div>

			{/* Main Content */}
			<div className="relative z-10 p-6">
				<div className="text-white text-2xl">
					Hello
				</div>
			</div>
		</div>
	)
}