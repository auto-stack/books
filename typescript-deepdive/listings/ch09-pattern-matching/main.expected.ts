// Auto — pattern matching and exhaustiveness
type Shape =
  | { _tag: "Circle"; value: number }
  | { _tag: "Rect"; value: [number, number] }
  | { _tag: "Triangle"; value: [number, number, number] };
const Shape = {
  Circle: (r: number) => ({ _tag: "Circle", value: r }),
  Rect: (w: number, h: number) => ({ _tag: "Rect", value: [w, h] }),
  Triangle: (a: number, b: number, c: number) => ({ _tag: "Triangle", value: [a, b, c] }),
};

type Option<T> =
  | { _tag: "Some"; value: T }
  | { _tag: "None" };
const Option = {
  Some: <T>(v: T) => ({ _tag: "Some", value: v }),
  None: () => ({ _tag: "None" }),
};

function area(s: Shape): number {
  switch (s._tag) {
    case "Circle": {
      const r = s.value;
      return 3.14159 * r * r;
    }
    case "Rect": {
      const [w, h] = s.value;
      return w * h;
    }
    case "Triangle": {
      const [a, b, c] = s.value;
      const s = (a + b + c) / 2.0;
      return Math.sqrt(s * (s - a) * (s - b) * (s - c));
    }
  }
}

function describe(s: Shape): string {
  switch (s._tag) {
    case "Circle": {
      const r = s.value;
      return "Circle(r=" + r + ")";
    }
    case "Rect": {
      const [w, h] = s.value;
      return "Rect(" + w + ", " + h + ")";
    }
    case "Triangle": {
      const [a, b, c] = s.value;
      return "Triangle(" + a + ", " + b + ", " + c + ")";
    }
  }
}

function process(value: number | string | boolean): void {
  switch (typeof value) {
    case "number":
      console.log("Integer: " + value);
      break;
    case "string":
      console.log("String length: " + (value as string).length);
      break;
    case "boolean":
      console.log(value ? "true" : "false");
      break;
  }
}

function main(): void {
  const shapes: Shape[] = [
    Shape.Circle(5.0),
    Shape.Rect(3.0, 4.0),
    Shape.Triangle(3.0, 4.0, 5.0),
  ];
  for (const shape of shapes) {
    console.log(describe(shape));
    console.log("  area = " + area(shape));
  }

  process(42);
  process("hello");
  process(true);
}

main();
