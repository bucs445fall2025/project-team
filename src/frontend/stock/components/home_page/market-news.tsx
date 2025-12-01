"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { Button } from "@/components/ui/button"

interface NewsItem {
	title: string
	summary: string
	link: string
	providerPublishTime: string
	publisher: string
}

function formatTimeAgo(dateInput: string | number) {
	const date = new Date(dateInput)
	const now = new Date()
	const seconds = Math.floor((now.getTime() - date.getTime()) / 1000)

	let interval = seconds / 31536000
	if (interval > 1) return Math.floor(interval) + " years ago"
	interval = seconds / 2592000
	if (interval > 1) return Math.floor(interval) + " months ago"
	interval = seconds / 86400
	if (interval > 1) return Math.floor(interval) + " days ago"
	interval = seconds / 3600
	if (interval > 1) return Math.floor(interval) + " hours ago"
	interval = seconds / 60
	if (interval > 1) return Math.floor(interval) + " minutes ago"
	return Math.floor(seconds) + " seconds ago"
}

export default function MarketNews() {
	const [newsItems, setNewsItems] = useState<NewsItem[]>([])
	const [loading, setLoading] = useState(true)
	const [error, setError] = useState<string | null>(null)
	const router = useRouter()

	useEffect(() => {
		const fetchNews = async () => {
			try {
				setLoading(true)
				setError(null)

				const response = await fetch('http://localhost:8000/api/market/news')
				if (!response.ok) {
					throw new Error('Failed to fetch market news. Please try again later.')
				}
				const data = await response.json()
				const sortedNews = (data.news || []).sort((a: NewsItem, b: NewsItem) => {
					return new Date(b.providerPublishTime).getTime() - new Date(a.providerPublishTime).getTime()
				})
				setNewsItems(sortedNews)
			} catch (err) {
				if (err instanceof Error) {
					setError(err.message)
				} else {
					setError("An unknown error occurred.")
				}
			} finally {
				setLoading(false)
			}
		}

		fetchNews()
	}, [])

	if (loading) {
		return (
			<Card className="h-full bg-white/10 backdrop-blur-lg border-white/20">
				<CardHeader>
					<CardTitle className="text-white">Market News</CardTitle>
				</CardHeader>
				<CardContent>
					<div className="space-y-4">
						{[...Array(6)].map((_, i) => (
							<div key={i} className="space-y-2 border-b border-white/10 pb-3 last:border-0 last:pb-0">
								<Skeleton className="h-5 w-3/4 bg-white/20" />
								<Skeleton className="h-4 w-full bg-white/20" />
								<div className="flex items-center justify-between pt-1">
									<Skeleton className="h-4 w-1/4 bg-white/20" />
									<Skeleton className="h-4 w-1/5 bg-white/20" />
								</div>
							</div>
						))}
					</div>
				</CardContent>
			</Card>
		)
	}

	if (error) {
		return (
			<Card className="flex h-96 w-full items-center justify-center bg-red-500/20 backdrop-blur-lg border-red-400/30">
				<div className="text-center">
					<CardTitle className="text-2xl text-red-400">Error</CardTitle>
					<CardDescription className="text-red-300">{error}</CardDescription>
					<Button
						variant="destructive"
						className="mt-4"
						onClick={() => router.back()}
					>
						Go Back
					</Button>
				</div>
			</Card>
		)
	}

	return (
		<Card className="h-full bg-white/10 backdrop-blur-lg border-white/20">
			<CardHeader>
				<CardTitle className="text-white">Market News</CardTitle>
			</CardHeader>
			<CardContent>
				<div className="space-y-4">
					{newsItems.length > 0 ? newsItems.map((item) => (
						<div key={item.link} className="border-b border-white/10 pb-3 last:border-0 last:pb-0">
							<a href={item.link} target="_blank" rel="noopener noreferrer" className="hover:underline">
								<h3 className="font-medium text-white">{item.title}</h3>
							</a>
							<p className="text-sm text-gray-300 pt-1">{item.summary}</p>
							<div className="flex items-center justify-between text-sm text-gray-400 pt-2">
								<span>{item.publisher}</span>
								<span>{formatTimeAgo(item.providerPublishTime)}</span>
							</div>
						</div>
					)) : (
						<p className="text-gray-400">No news available at the moment.</p>
					)}
				</div>
			</CardContent>
		</Card>
	)
}