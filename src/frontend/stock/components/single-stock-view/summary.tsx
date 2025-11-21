import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../ui/card";
import ReactMarkdown from 'react-markdown';

export default function Summary({ ticker }: { ticker: string }) {
	const [summary, setSummary] = useState<string>('');
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState<string | null>(null);

	useEffect(() => {
		const fetchSummary = async () => {
			if (!ticker) return;

			setLoading(true);
			setError(null);

			try {
				const response = await fetch(`http://localhost:8000/api/stock/${ticker}/summary`);

				if (!response.ok) {
					throw new Error(`Failed to fetch summary: ${response.statusText}`);
				}

				const data = await response.text();
				// Replace literal \n with actual newlines
				const formattedData = data.replace(/\\n/g, '\n');
				setSummary(formattedData);
			} catch (err) {
				setError(err instanceof Error ? err.message : 'An error occurred');
			} finally {
				setLoading(false);
			}
		};

		fetchSummary();
	}, [ticker]);

	return (
		<Card className="h-96 overflow-hidden flex flex-col">
			<CardHeader>
				<CardTitle>Summary</CardTitle>
			</CardHeader>
			<CardContent className="flex-1 overflow-y-scroll">
				{loading && (
					<div className="flex items-center justify-center h-full">
						<div className="animate-pulse text-muted-foreground">Loading summary...</div>
					</div>
				)}

				{error && (
					<div className="text-destructive text-sm">
						Error: {error}
					</div>
				)}

				{!loading && !error && summary && (
					<div className="prose prose-sm dark:prose-invert max-w-none">
						<ReactMarkdown
							components={{
								h1: ({ node, ...props }: any) => <h1 className="text-xl font-bold mb-3" {...props} />,
								h2: ({ node, ...props }: any) => <h2 className="text-lg font-semibold mb-2 mt-4" {...props} />,
								h3: ({ node, ...props }: any) => <h3 className="text-base font-semibold mb-2 mt-3" {...props} />,
								p: ({ node, ...props }: any) => <p className="mb-3 leading-relaxed" {...props} />,
								ul: ({ node, ...props }: any) => <ul className="list-disc list-inside mb-3 space-y-1" {...props} />,
								ol: ({ node, ...props }: any) => <ol className="list-decimal list-inside mb-3 space-y-1" {...props} />,
								li: ({ node, ...props }: any) => <li className="ml-2" {...props} />,
								strong: ({ node, ...props }: any) => <strong className="font-semibold" {...props} />,
								em: ({ node, ...props }: any) => <em className="italic" {...props} />,
								code: ({ node, ...props }: any) => (
									<code className="bg-muted px-1.5 py-0.5 rounded text-sm font-mono" {...props} />
								),
							}}
						>
							{summary}
						</ReactMarkdown>
					</div>
				)}

				{!loading && !error && !summary && (
					<div className="text-muted-foreground text-sm">
						No summary available
					</div>
				)}
			</CardContent>
		</Card>
	);
}