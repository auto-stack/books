// Book Listing Test Harness
// Provides runner functions for each transpilation/execution mode.
// Each runner reads main.at from a listing directory, transpiles/executes it,
// and compares the output against .expected.* files.

use std::fs;
use std::path::Path;

// ---------------------------------------------------------------------------
// a2r: Auto -> Rust
// ---------------------------------------------------------------------------
pub fn run_a2r(listing_dir: &Path) -> Result<(), String> {
    let at_path = listing_dir.join("main.at");
    let exp_path = listing_dir.join("main.expected.rs");

    let src = fs::read_to_string(&at_path)
        .map_err(|e| format!("read {}: {e}", at_path.display()))?;
    let expected = fs::read_to_string(&exp_path)
        .map_err(|e| format!("read {}: {e}", exp_path.display()))?;

    let name = listing_dir
        .file_name()
        .unwrap_or_default()
        .to_str()
        .unwrap_or("main");

    let mut sink = auto_lang::trans::rust::transpile_rust(name, &src)
        .map_err(|e| format!("transpile_rust: {e}"))?;
    let actual = String::from_utf8_lossy(sink.done().map_err(|e| format!("sink.done: {e}"))?).to_string();

    if actual != expected {
        let wrong_path = listing_dir.join("main.wrong.rs");
        let _ = fs::write(&wrong_path, &actual);
        return Err(format!(
            "a2r mismatch for {}. See main.wrong.rs",
            listing_dir.display()
        ));
    }

    Ok(())
}

// ---------------------------------------------------------------------------
// a2c: Auto -> C
// ---------------------------------------------------------------------------
pub fn run_a2c(listing_dir: &Path) -> Result<(), String> {
    let at_path = listing_dir.join("main.at");
    let exp_c_path = listing_dir.join("main.expected.c");
    let exp_h_path = listing_dir.join("main.expected.h");

    let src = fs::read_to_string(&at_path)
        .map_err(|e| format!("read {}: {e}", at_path.display()))?;

    let name = listing_dir
        .file_name()
        .unwrap_or_default()
        .to_str()
        .unwrap_or("main");

    let mut sink = auto_lang::trans::c::transpile_c(name, &src)
        .map_err(|e| format!("transpile_c: {e}"))?;
    let actual_source = String::from_utf8_lossy(sink.done().map_err(|e| format!("sink.done: {e}"))?).to_string();
    let actual_header = String::from_utf8_lossy(&sink.header).to_string();

    // Compare C source
    if exp_c_path.exists() {
        let expected_c = fs::read_to_string(&exp_c_path)
            .map_err(|e| format!("read {}: {e}", exp_c_path.display()))?;
        if actual_source != expected_c {
            let wrong_path = listing_dir.join("main.wrong.c");
            let _ = fs::write(&wrong_path, &actual_source);
            return Err(format!(
                "a2c source mismatch for {}. See main.wrong.c",
                listing_dir.display()
            ));
        }
    }

    // Compare C header (only if expected.h exists)
    if exp_h_path.exists() {
        let expected_h = fs::read_to_string(&exp_h_path)
            .map_err(|e| format!("read {}: {e}", exp_h_path.display()))?;
        if actual_header != expected_h {
            let wrong_path = listing_dir.join("main.wrong.h");
            let _ = fs::write(&wrong_path, &actual_header);
            return Err(format!(
                "a2c header mismatch for {}. See main.wrong.h",
                listing_dir.display()
            ));
        }
    }

    Ok(())
}

// ---------------------------------------------------------------------------
// a2p: Auto -> Python
// ---------------------------------------------------------------------------
pub fn run_a2p(listing_dir: &Path) -> Result<(), String> {
    use auto_lang::trans::{Sink, Trans};
    use auto_lang::trans::python::PythonTrans;
    use auto_lang::parser::Parser;

    let at_path = listing_dir.join("main.at");
    let exp_path = listing_dir.join("main.expected.py");

    let src = fs::read_to_string(&at_path)
        .map_err(|e| format!("read {}: {e}", at_path.display()))?;
    let expected = fs::read_to_string(&exp_path)
        .map_err(|e| format!("read {}: {e}", exp_path.display()))?;

    let name = listing_dir
        .file_name()
        .unwrap_or_default()
        .to_str()
        .unwrap_or("main");

    let mut parser = Parser::from(src.as_str());
    let ast = parser.parse().map_err(|e| format!("parse: {e}"))?;
    let mut sink = Sink::new(name.into());
    let mut trans = PythonTrans::new(name.into());
    trans.trans(ast, &mut sink).map_err(|e| format!("trans: {e}"))?;
    let actual = String::from_utf8_lossy(sink.done().map_err(|e| format!("sink.done: {e}"))?).to_string();

    if actual != expected {
        let wrong_path = listing_dir.join("main.wrong.py");
        let _ = fs::write(&wrong_path, &actual);
        return Err(format!(
            "a2p mismatch for {}. See main.wrong.py",
            listing_dir.display()
        ));
    }

    Ok(())
}

// ---------------------------------------------------------------------------
// a2ts: Auto -> TypeScript
// ---------------------------------------------------------------------------
pub fn run_a2ts(listing_dir: &Path) -> Result<(), String> {
    use auto_lang::trans::{Sink, Trans};
    use auto_lang::trans::typescript::TypeScriptTrans;
    use auto_lang::parser::Parser;

    let at_path = listing_dir.join("main.at");
    let exp_path = listing_dir.join("main.expected.ts");

    let src = fs::read_to_string(&at_path)
        .map_err(|e| format!("read {}: {e}", at_path.display()))?;
    let expected = fs::read_to_string(&exp_path)
        .map_err(|e| format!("read {}: {e}", exp_path.display()))?;

    let name = listing_dir
        .file_name()
        .unwrap_or_default()
        .to_str()
        .unwrap_or("main");

    let mut parser = Parser::from(src.as_str());
    let ast = parser.parse().map_err(|e| format!("parse: {e}"))?;
    let mut sink = Sink::new(name.into());
    let mut trans = TypeScriptTrans::new(name.into());
    trans.trans(ast, &mut sink).map_err(|e| format!("trans: {e}"))?;
    let actual = String::from_utf8_lossy(sink.done().map_err(|e| format!("sink.done: {e}"))?).to_string();

    if actual != expected {
        let wrong_path = listing_dir.join("main.wrong.ts");
        let _ = fs::write(&wrong_path, &actual);
        return Err(format!(
            "a2ts mismatch for {}. See main.wrong.ts",
            listing_dir.display()
        ));
    }

    Ok(())
}

// ---------------------------------------------------------------------------
// vm: AutoVM execution
// ---------------------------------------------------------------------------
pub fn run_vm(listing_dir: &Path) -> Result<(), String> {
    let at_path = listing_dir.join("main.at");

    let src = fs::read_to_string(&at_path)
        .map_err(|e| format!("read {}: {e}", at_path.display()))?;

    // Check for .expected.error first
    let err_path = listing_dir.join("main.expected.error");
    if err_path.exists() {
        let result = auto_lang::run(&src);
        if result.is_ok() {
            return Err(format!(
                "vm: expected error but succeeded for {}",
                listing_dir.display()
            ));
        }
        return Ok(());
    }

    let (result, stdout) = auto_lang::run_with_capture(&src)
        .map_err(|e| format!("vm run: {e}"))?;

    // Check .expected.out (stdout)
    let out_path = listing_dir.join("main.expected.out");
    if out_path.exists() {
        let expected_out = fs::read_to_string(&out_path)
            .map_err(|e| format!("read {}: {e}", out_path.display()))?;
        if stdout != expected_out {
            let wrong_path = listing_dir.join("main.wrong.out");
            let _ = fs::write(&wrong_path, &stdout);
            return Err(format!(
                "vm stdout mismatch for {}. See main.wrong.out",
                listing_dir.display()
            ));
        }
    }

    // Check .expected.result (return value)
    let res_path = listing_dir.join("main.expected.result");
    if res_path.exists() {
        let expected_res = fs::read_to_string(&res_path)
            .map_err(|e| format!("read {}: {e}", res_path.display()))?;
        if result != expected_res {
            let wrong_path = listing_dir.join("main.wrong.result");
            let _ = fs::write(&wrong_path, &result);
            return Err(format!(
                "vm result mismatch for {}. See main.wrong.result",
                listing_dir.display()
            ));
        }
    }

    Ok(())
}
