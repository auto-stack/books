// TypeScript

function main(): void {
    const nums: number[] = [3, 1, 4, 1, 5, 9, 2, 6];
    const sorted: number[] = [...nums].sort((a, b) => a - b);
    for (const n of sorted) {
        console.log(n);
    }

    const rev: number[] = [1, 2, 3, 4, 5].reverse();
    console.log(rev);

    const uniq: number[] = [...new Set([3, 1, 4, 1, 5, 9, 2, 6, 5, 3])];
    console.log(uniq);

    const flat: number[] = [[1, 2], [3, 4], [5, 6]].flat();
    console.log(flat);

    const names: string[] = ["Alice", "Bob", "Carol"];
    const scores: number[] = [95, 87, 92];
    const pairs: [string, number][] = names.map((n, i) => [n, scores[i]]);
    for (const pair of pairs) {
        console.log(pair);
    }

    const data: number[] = [1, 2, 3, 4, 5, 6, 7];
    const chunked: number[][] = [];
    for (let i = 0; i < data.length; i += 3) {
        chunked.push(data.slice(i, i + 3));
    }
    for (const c of chunked) {
        console.log(c);
    }
}

main();
