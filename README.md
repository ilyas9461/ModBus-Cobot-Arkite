# ModBus-Cobot-Arkite
**Working Schema Explanation: Arkite OOS ↔ UR5 Cobot (via MODBUS TCP/IP)**

**1. System Overview:**
- **Arkite OOS (Operator Support System)**: Acts as the **MODBUS TCP Client**.
- **UR5 Cobot**: Acts as the **MODBUS TCP Server**.
- **Communication Protocol**: MODBUS TCP/IP over Ethernet.

<p align="center">
    <img src="images/Arkite_UR5_Modbus_Schema.jpg" width="50%">
</p>


**2. Communication Flow:**

**Step 1 – Command Transmission:**
- The Arkite OOS sends a **movement command** or **action request** to the UR5 robot.
- This command is written into the **holding register 128** on the UR5 server.
  - Example: `Register 128 = 101` (Move to Position 1)

**Step 2 – UR5 Execution:**
- The UR5 continuously runs a **thread** that monitors (reads) the value of **register 128**.
- When a new value is detected in register 128, the UR5 interprets it as a new command.
- The UR5 then performs the corresponding action, such as moving to a specified position.

**Step 3 – Result Feedback:**
- Once the action is completed, the UR5 updates **holding register 133** with a **status code or result**.
  - Example: `Register 133 = 1` → Action completed successfully.
  - Example: `Register 133 = 0` → Error or command not executed.

**Step 4 – Arkite Status Check:**
- The Arkite OOS reads **register 133** to verify the result of the previous command.
- Based on the value in register 133, the Arkite may:
  - Continue to the next instruction.
  - Retry the command.
  - Display a message to the operator.

**3. Summary of Register Usage:**
| Device | Role  | Register | Direction | Purpose |
|---------|-------|-----------|------------|----------|
| Arkite OOS | Client | 128 | Write → UR5 | Command request |
| UR5 Cobot | Server | 133 | Read ← Arkite | Execution result |

**4. Thread Behavior (UR5):**
- The UR5 runs a background thread that:
  1. Periodically polls register 128.
  2. Detects changes in value (new commands).
  3. Executes corresponding robot motions.
  4. Writes back the completion or status to register 133.

**5. Communication Timing Diagram (Simplified):**

```
Arkite (Client)              UR5 (Server)
     |                            |
     | Write: Command(128=101)    |
     |--------------------------->|
     |                            |  [Thread detects new command]
     |                            |  Execute Move(Position1)
     |                            |  Write Result(133=1)
     |<---------------------------|
     | Read: Status(133=1)        |
     |                            |
```

**6. Optional Enhancements:**
- Add additional registers for:
  - Error codes
  - Real-time position feedback
  - Command queueing
- Use proper synchronization in the UR5 thread to prevent data race.

---

Would you like me to generate a **.drawio file** that visually represents this communication flow with all components (Arkite, UR5, MODBUS TCP/IP, registers, and thread process)?


