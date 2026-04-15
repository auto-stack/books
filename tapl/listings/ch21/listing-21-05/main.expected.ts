// TypeScript

function formatDuration(ms: number): string {
    const totalSec = Math.floor(ms / 1000);
    const h = Math.floor(totalSec / 3600);
    const m = Math.floor((totalSec % 3600) / 60);
    return `${h}h ${m}m`;
}

function main(): void {
    const now: Date = new Date();
    console.log(now.toISOString());

    const formatted: string = now.toISOString().replace("T", " ").slice(0, 19);
    console.log(formatted);

    const parsed: Date = new Date("2025-01-15T10:30:00");
    console.log(parsed.toISOString());

    const durationMs: number = (2 * 3600 + 30 * 60) * 1000;
    console.log(formatDuration(durationMs));

    const later: Date = new Date(now.getTime() + durationMs);
    console.log(later.toISOString());

    const diffMin: number = Math.round((later.getTime() - now.getTime()) / 60000);
    console.log(diffMin);
}

main();
