// Auto — this file demonstrates the compilation pipeline
// The Auto compiler transforms this source through these stages:
//
// 1. SCANNER:  Converts text to tokens
//    "fn add(a int, b int) int { a + b }"
//    → [FnKeyword, Identifier("add"), LParen, Identifier("a"),
//       IntKeyword, Comma, Identifier("b"), IntKeyword, RParen,
//       IntKeyword, LBrace, Identifier("a"), Plus, Identifier("b"), RBrace]
//
// 2. PARSER:   Converts tokens to AST
//    → FunctionDecl(name: "add", params: [Param("a", int), Param("b", int)],
//                    return_type: int, body: BinaryExpr(Ident("a"), Plus, Ident("b")))
//
// 3. BINDER:   Creates symbols from AST declarations
//    → Symbol("add"), Symbol("a"), Symbol("b")
//
// 4. CHECKER:  Validates types and resolves generics
//    → int + int = int ✓ (return type matches annotation)
//
// 5. EMITTER:  Generates TypeScript output
//    → function add(a: number, b: number): number { return a + b; }

function add(a: number, b: number): number {
    return a + b;
}

function main(): void {
    console.log("add(3, 4) = " + add(3, 4));
}

main();
