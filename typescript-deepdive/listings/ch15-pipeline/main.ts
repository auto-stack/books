// TypeScript — the TypeScript compiler pipeline
// This file demonstrates the TypeScript compilation stages:
//
// 1. SCANNER:  Converts text to tokens
//    "function add(a: number, b: number): number { return a + b; }"
//    → [FunctionKeyword, Identifier("add"), LParen, Identifier("a"),
//       Colon, NumberKeyword, Comma, Identifier("b"), Colon,
//       NumberKeyword, RParen, Colon, NumberKeyword, LBrace,
//       ReturnKeyword, Identifier("a"), Plus, Identifier("b"), Semicolon, RBrace]
//
// 2. PARSER:   Converts tokens to AST
//    → FunctionDeclaration(name: "add", params: [...], returnType: NumberKeyword,
//                          body: Block(ReturnStatement(BinaryExpression(...))))
//
// 3. BINDER:   Creates symbols for all declarations
//    → Symbol("add", flags: Function), Symbol("a"), Symbol("b")
//
// 4. CHECKER:  Type checks and validates
//    → number + number = number ✓
//
// 5. EMITTER:  Generates JavaScript output
//    → function add(a, b) { return a + b; }

function add(a: number, b: number): number {
    return a + b;
}

console.log("add(3, 4) = " + add(3, 4));
