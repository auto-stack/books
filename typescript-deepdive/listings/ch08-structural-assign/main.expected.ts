// Auto — structural type compatibility
class Point2D {
  x: number;
  y: number;
  constructor(x: number, y: number) {
    this.x = x;
    this.y = y;
  }
}

class Point3D {
  x: number;
  y: number;
  z: number;
  constructor(x: number, y: number, z: number) {
    this.x = x;
    this.y = y;
    this.z = z;
  }
}

function print_x(p: Point2D): void {
  console.log("x = " + p.x);
}

class Named {
  name: string;
  constructor(name: string) {
    this.name = name;
  }
}

class Employee {
  name: string;
  role: string;
  constructor(name: string, role: string) {
    this.name = name;
    this.role = role;
  }
}

function greet(n: Named): void {
  console.log("Hello, " + n.name);
}

function main(): void {
  const p2 = new Point2D(1.0, 2.0);
  const p3 = new Point3D(1.0, 2.0, 3.0);

  print_x(p2);   // exact match
  print_x(p3);   // OK — extra field is fine (structural)

  const emp = new Employee("Alice", "Engineer");
  greet(emp);    // OK — Employee has `name` field
}

main();
