import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

const execute = promisify(execFile);
const labDirectory = fileURLToPath(new URL("../../", import.meta.url));
const mutatingTools = new Set(["edit", "write", "apply_patch", "multiedit"]);

// OpenCode 1.18.31 plugin API. The trusted runner is never supplied by the model.
export const CheckAfterEdit = async () => ({
  "tool.execute.after": async (input, output) => {
    if (!mutatingTools.has(input.tool)) return;
    let status = "PASS";
    let details;
    try {
      const result = await execute("sh", ["scripts/check.sh", "all"], {
        cwd: labDirectory, timeout: 65000, maxBuffer: 1024 * 1024,
      });
      details = result.stdout + result.stderr;
    } catch (error) {
      status = "FAIL";
      details = (error.stdout || "") + (error.stderr || "") + "\n" + error.message;
    }
    output.output += `\n\n[AUTO-CHECK ${status}]\n${details}`;
  },
});
