// TypeScript — type guards and narrowing
type Shape =
    | { kind: "circle"; radius: number }
    | { kind: "rect"; width: number; height: number }
    | { kind: "triangle"; a: number; b: number; c: number };

function area(s: Shape): number {
    switch (s.kind) {
        case "circle":
            return Math.PI * s.radius * s.radius;
        case "rect":
            return s.width * s.height;
        case "triangle":
            const p = (s.a + s.b + s.c) / 2;
            return Math.sqrt(p * (p - s.a) * (p - s.b) * (p - s.c));
    }
}

function describe(s: Shape): string {
    switch (s.kind) {
        case "circle": return `Circle(r=${s.radius})`;
        case "rect": return `Rect(${s.width}, ${s.height})`;
        case "triangle": return `Triangle(${s.a}, ${s.b}, ${s.c})`;
    }
}

function process(value: number | string | boolean): void {
    if (typeof value === "number") {
        console.log("Integer: " + value);
    } else if (typeof value === "string") {
        console.log("String length: " + value.length);
    } else {
        console.log(value ? "true" : "false");
    }
}

const shapes: Shape[] = [
    { kind: "circle", radius: 5 },
    { kind: "rect", width: 3, height: 4 },
    { kind: "triangle", a: 3, b: 4, c: 5 }
];
for (const shape of shapes) {
    console.log(describe(shape));
    console.log("  area = " + area(shape));
}

process(42);
process("hello");
process(true);
