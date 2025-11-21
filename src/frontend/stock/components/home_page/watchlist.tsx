"use client"
import { ArrowDownIcon, ArrowUpIcon, StarIcon } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"

export default function Watchlist() {
	const [isLoggedIn, setIsLoggedIn] = useState(false)
	const [watchlistItems, setWatchlistItems] = useState([])
	const [loading, setLoading] = useState(true)
	const router = useRouter()

	useEffect(() => {
		// Check if user is logged in by looking for token in cookies
		const token = document.cookie
			.split('; ')
			.find(row => row.startsWith('token='))
			?.split('=')[1]

		if (!token) {
			setIsLoggedIn(false)
			setLoading(false)
			return
		}

		setIsLoggedIn(true)

		// Fetch watchlist from API
		fetch('http://localhost:8000/api/user/watchlist', {
			headers: {
				'Authorization': `Bearer ${token}`
			}
		})
			.then(res => res.json())
			.then(data => {
				setWatchlistItems(data)
				setLoading(false)
			})
			.catch(err => {
				console.error('Error fetching watchlist:', err)
				setLoading(false)
			})
	}, [])

	const handleRowClick = (symbol: string) => {
		router.push(`/stock/${symbol}`)
	}

	return (
		<Card className="h-full bg-white/10 backdrop-blur-lg border-white/20">
			<CardHeader className="flex flex-row items-center justify-between">
				<CardTitle>Watchlist</CardTitle>
				<StarIcon className="h-5 w-5 text-yellow-500" />
			</CardHeader>
			<CardContent>
				{!isLoggedIn ? (
					<div className="text-center py-8 text-muted-foreground">
						You are not logged in, sign in
					</div>
				) : loading ? (
					<div className="text-center py-8 text-muted-foreground">
						Loading...
					</div>
				) : (
					<Table>
						<TableHeader>
							<TableRow>
								<TableHead>Symbol</TableHead>
								<TableHead className="text-right">Price</TableHead>
								<TableHead className="text-right">Change</TableHead>
							</TableRow>
						</TableHeader>
						<TableBody>
							{watchlistItems.map((item: any) => (
								<TableRow
									key={item.symbol}
									onClick={() => handleRowClick(item.symbol)}
									className="cursor-pointer hover:bg-white/5"
								>
									<TableCell>
										<div>
											<div className="font-medium">{item.symbol}</div>
											<div className="text-xs text-muted-foreground">{item.name}</div>
										</div>
									</TableCell>
									<TableCell className="text-right">${item.price.toFixed(2)}</TableCell>
									<TableCell className="text-right">
										<div className={item.change >= 0 ? "text-green-500" : "text-red-500"}>
											<div className="flex items-center justify-end">
												{item.change >= 0 ? (
													<ArrowUpIcon className="mr-1 h-4 w-4" />
												) : (
													<ArrowDownIcon className="mr-1 h-4 w-4" />
												)}
												{item.percentChange.toFixed(2)}%
											</div>
										</div>
									</TableCell>
								</TableRow>
							))}
						</TableBody>
					</Table>
				)}
			</CardContent>
		</Card>
	)
}