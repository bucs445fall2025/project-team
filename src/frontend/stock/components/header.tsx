"use client"
import { useState, useEffect } from 'react'
import { usePathname } from 'next/navigation'
import Link from 'next/link'
import { TrendingUp } from 'lucide-react'
import { Button } from "@/components/ui/button"

export default function Header() {
	const [firstName, setFirstName] = useState('')
	const pathname = usePathname()
	const excludedPaths = ['/', '/signup', '/login']
	const shouldShowHeader = !excludedPaths.includes(pathname)

	useEffect(() => {
		if (!shouldShowHeader) return

		const fetchFirstName = async () => {
			try {
				const token = document.cookie
					.split('; ')
					.find(row => row.startsWith('token='))
					?.split('=')[1]

				if (!token) {
					// console.error('No token found')
					// Leave firstName as empty string to trigger the Stranger/Login state
					return
				}
				const response = await fetch('http://localhost:8000/api/auth/getFirstName', {
					method: 'GET',
					headers: {
						'Authorization': `Bearer ${token}`,
						'Content-Type': 'application/json',
					},
				})

				if (response.ok) {
					const data = await response.json()
					const name = data.firstName || data.first || 'Stranger'
					setFirstName(name)
				} else {
					console.error('Failed to fetch first name:', response.status)
				}
			} catch (error) {
				console.error('Error fetching first name:', error)
			}
		}

		fetchFirstName()
	}, [shouldShowHeader])

	if (!shouldShowHeader) {
		return null
	}

	const isStranger = !firstName || firstName === 'Stranger'

	return (
		<div className="backdrop-blur-xl border-b border-blue-400/20 sticky top-0 z-50 shadow-2xl shadow-blue-500/20">
			<div className="flex items-center justify-between px-6 py-4">
				{/* Logo */}
				<Link href="/dashboard" className="flex items-center space-x-2 transition-opacity hover:opacity-80">
					<div className="bg-gradient-to-br from-blue-500 to-cyan-500 p-2 rounded-lg">
						<TrendingUp className="w-6 h-6 text-white" />
					</div>
					<span className="text-2xl font-bold text-white">Pelosi's Stash</span>
				</Link>

				{/* User Greeting or Login Button */}
				<div className="text-white font-medium">
					{isStranger ? (
						<Link href="/login">
							<button
								className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition">
								Sign In
							</button>
						</Link>
					) : (
						<span>Hello {firstName}</span>
					)}
				</div>
			</div>
		</div>
	)
}