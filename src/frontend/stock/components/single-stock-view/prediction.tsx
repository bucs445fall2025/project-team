import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../ui/card";
import { TrendingUp, TrendingDown } from 'lucide-react';

interface ModelPrediction {
	model_name: string;
	predicted_price: number;
}

interface PredictionData {
	recommendation: 'BUY' | 'SELL' | 'HOLD';
	current_price: number;
	predictions: ModelPrediction[];
}

export default function Prediction({ ticker }: { ticker: string }) {
	const [data, setData] = useState<PredictionData | null>(null);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState<string | null>(null);

	useEffect(() => {
		const fetchPrediction = async () => {
			if (!ticker) return;

			setLoading(true);
			setError(null);

			try {
				const response = await fetch(`http://localhost:8000/api/predict/${ticker}`);

				if (!response.ok) {
					throw new Error(`Failed to fetch predictions: ${response.statusText}`);
				}

				const result = await response.json();
				setData(result);
			} catch (err) {
				setError(err instanceof Error ? err.message : 'An error occurred');
			} finally {
				setLoading(false);
			}
		};

		fetchPrediction();
	}, [ticker]);

	const calculatePercentageChange = (predictedPrice: number) => {
		if (!data?.current_price) return 0;
		return ((predictedPrice - data.current_price) / data.current_price) * 100;
	};

	const getRecommendationColor = (recommendation: string) => {
		switch (recommendation) {
			case 'BUY': return 'text-green-600 dark:text-green-400';
			case 'SELL': return 'text-red-600 dark:text-red-400';
			case 'HOLD': return 'text-yellow-600 dark:text-yellow-400';
			default: return 'text-gray-600';
		}
	};

	return (
		<Card className="h-96 overflow-hidden flex flex-col">
			<CardHeader>
				<CardTitle>Recommendation</CardTitle>
			</CardHeader>
			<CardContent className="flex-1 overflow-y-scroll">
				{loading && (
					<div className="flex items-center justify-center h-full">
						<div className="animate-pulse text-muted-foreground">Loading predictions...</div>
					</div>
				)}

				{error && (
					<div className="text-destructive text-sm">
						Error: {error}
					</div>
				)}

				{!loading && !error && data && (
					<div className="space-y-6">
						<div className={`text-6xl font-bold text-center py-4 ${getRecommendationColor(data.recommendation)}`}>
							{data.recommendation}
						</div>

						<div className="space-y-3">
							{data.predictions.map((prediction, index) => {
								const percentChange = calculatePercentageChange(prediction.predicted_price);
								const isPositive = percentChange >= 0;

								return (
									<div
										key={index}
										className="flex items-center justify-between p-3 rounded-lg bg-muted/50 hover:bg-muted transition-colors"
									>
										<span className="font-medium text-sm">{prediction.model_name}</span>
										<div className="flex items-center gap-2">
											<span className="text-sm font-medium text-muted-foreground">
												${prediction.predicted_price.toFixed(2)}
											</span>
											{isPositive ? (
												<TrendingUp className="w-5 h-5 text-green-600 dark:text-green-400" />
											) : (
												<TrendingDown className="w-5 h-5 text-red-600 dark:text-red-400" />
											)}
											<span className={`font-semibold text-sm ${isPositive ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>
												{isPositive ? '+' : ''}{percentChange.toFixed(2)}%
											</span>
										</div>
									</div>
								);
							})}
						</div>
					</div>
				)}

				{!loading && !error && !data && (
					<div className="text-muted-foreground text-sm">
						No predictions available
					</div>
				)}
			</CardContent>
		</Card>
	);
}