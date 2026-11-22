# FactoryOps — Safety Procedures

## 1. Purpose

This document contains the safety and operating procedures currently seeded in FactoryOps.

The application contains four verified SOPs:

| SOP ID | SOP Name | Version |
|---|---|---|
| SOP-CNC-501 | CNC Machine Operating Procedure | 3.2 |
| SOP-PRS-402 | Hydraulic Press Operating Procedure | 2.8 |
| SOP-ROB-303 | Robotic Welding Operating Procedure | 4.0 |
| SOP-EMG-101 | Emergency Machine Shutdown Procedure | 5.1 |

These procedures are available through the FactoryOps SOP module.

**Important:** These are the four procedures verified in the inspected application source. They do not constitute a complete factory-wide safety manual.

---

## 2. SOP-CNC-501 — CNC Machine Operating Procedure

**Version:** 3.2

### Verified operating requirements

| Parameter | Requirement |
|---|---|
| Pneumatic pressure | Greater than 6.0 bar |
| Spindle warm-up starting speed | 500 RPM |
| Spindle warm-up ending speed | 3000 RPM |
| Warm-up duration | 8 minutes |
| Probe runout | Less than 0.003 mm |
| Coolant sump level | Greater than 75% |
| Personal protective equipment | Eye and ear protection within 5 metres |
| Machine interlocks | Must never be bypassed |

### Important precautions

- Maintain pneumatic pressure above 6.0 bar.
- Perform spindle warm-up from 500 RPM to 3000 RPM over 8 minutes.
- Verify probe runout is below 0.003 mm.
- Maintain coolant sump level above 75%.
- Ensure eye and ear protection is available within 5 metres.
- Never bypass machine safety interlocks.

### RAG retrieval keywords

CNC, spindle warm-up, pneumatic pressure, probe runout, coolant sump, eye protection, ear protection, machine interlocks.

---

## 3. SOP-PRS-402 — Hydraulic Press Operating Procedure

**Version:** 2.8

### Verified operating requirements

| Area | Requirement |
|---|---|
| Mechanical slide | Use mechanical slide lock pins |
| Hydraulic accumulator | Depressurize to 0 bar |
| Lifting equipment | Four-leg wire rope sling |
| Sling capacity | At least 5 metric tons |
| Electrical isolation | Apply LOTO on the 415V breaker |
| Press controls | Verify dual palm pushbuttons |
| Safety protection | Verify light curtain operation |

### Important precautions

- Use mechanical slide lock pins.
- Depressurize the hydraulic accumulator to 0 bar.
- Use a four-leg wire rope sling with a capacity of at least 5 metric tons.
- Apply Lockout/Tagout (LOTO) on the 415V breaker.
- Verify dual palm pushbuttons.
- Verify light curtain operation.

### RAG retrieval keywords

Hydraulic press, accumulator, zero pressure, slide lock pins, lifting sling, 415V breaker, LOTO, palm pushbuttons, light curtain.

---

## 4. SOP-ROB-303 — Robotic Welding Operating Procedure

**Version:** 4.0

### Verified operating requirements

| Area | Requirement |
|---|---|
| Robot operating mode | Teach mode |
| Emergency stop | E-stop depressed |
| Post-weld torch temperature | Above 200°C |
| Post-weld duration | 20 minutes |
| Shielding gas composition | 82% Argon / 18% CO2 |
| Gas safety | Inspect for leaks |
| Welding protection | UV-rated interlocked curtains |

### Important precautions

- Use Teach mode.
- Keep the E-stop depressed as specified by the procedure.
- Account for the hot torch condition above 200°C for 20 minutes after welding.
- Inspect shielding gas connections for leaks.
- Maintain the specified gas composition of 82% Argon and 18% CO2.
- Use UV-rated interlocked welding curtains.

### RAG retrieval keywords

Robotic welding, Teach mode, E-stop, hot torch, post-weld temperature, shielding gas, Argon, CO2, gas leakage, UV curtains.

---

## 5. SOP-EMG-101 — Emergency Machine Shutdown Procedure

**Version:** 5.1

### Verified emergency requirements

| Area | Requirement |
|---|---|
| Emergency response | Immediate E-stop |
| Notification | Alert supervisor and emergency beacon |
| Electrical isolation | Electrical disconnect |
| Lockout | Red LOTO padlock |
| Stored energy | Dissipate kinetic and hydraulic energy |
| Jam clearing | Dissipate stored energy before clearing jams |
| Restricted area | Maintain 3-metre quarantine perimeter |

### Emergency procedure requirements

1. Activate the emergency stop immediately.
2. Alert the supervisor.
3. Activate the emergency beacon.
4. Disconnect the electrical supply.
5. Apply the red LOTO padlock.
6. Dissipate stored kinetic and hydraulic energy before clearing jams.
7. Maintain a 3-metre quarantine perimeter.

### Important precautions

- Do not begin clearing a jam before stored energy has been dissipated.
- Maintain the 3-metre quarantine perimeter.
- Ensure electrical isolation and LOTO requirements are addressed.

### RAG retrieval keywords

Emergency shutdown, E-stop, emergency beacon, supervisor notification, electrical disconnect, red LOTO padlock, stored energy, hydraulic energy, machine jam, quarantine perimeter.

---

## 6. Lockout/Tagout (LOTO)

The verified SOPs contain specific LOTO-related requirements.

| SOP | Verified LOTO Requirement |
|---|---|
| SOP-PRS-402 | Apply LOTO on the 415V breaker. |
| SOP-EMG-101 | Electrical disconnect and red LOTO padlock. |

### Important limitation

A complete plant-wide LOTO master policy is not available in the inspected application source.

The following information remains missing or requires approval:

- Complete isolation procedures for every machine.
- Authorized personnel and approval responsibilities.
- Full lock and tag application/removal process.
- Group LOTO procedures.
- Verification and inspection requirements.
- Machine-specific stored-energy isolation details.

The RAG assistant must not invent these missing requirements.

---

## 7. Personal Protective Equipment (PPE)

The verified SOPs contain the following PPE-related requirements:

| SOP | Verified Requirement |
|---|---|
| SOP-CNC-501 | Eye and ear protection within 5 metres. |
| SOP-ROB-303 | UV-rated interlocked welding curtains. |

### Missing PPE information

The inspected source does not provide a complete PPE matrix.

The following information requires authorized safety-team input:

- PPE requirements for each production line.
- PPE requirements for chemical handling.
- PPE requirements for thermal hazards.
- PPE requirements for hydraulic and pneumatic work.
- Mandatory PPE by machine and work zone.
- Approved PPE specifications.

Do not present an assumed PPE matrix as official FactoryOps policy.

---

## 8. Missing Safety Documentation

Only four short seeded SOPs are currently verified.

The following safety documentation is missing or requires approval.

| Area | Missing Information | Status |
|---|---|---|
| Coating and Packaging | Line 4 operating and safety SOPs | MISSING |
| Chemical hazards | Detailed chemical handling procedures | MISSING |
| Thermal hazards | Detailed thermal hazard protocols | MISSING |
| Pneumatic hazards | Complete pneumatic safety procedures | MISSING |
| LOTO | Plant-wide LOTO master policy | MISSING |
| PPE | Complete PPE matrix by zone | MISSING |
| Confined spaces | Confined-space entry procedures and permits | MISSING |
| Hot work | Hot-work permit procedures | MISSING |
| Environmental compliance | Approved environmental procedures | MISSING |
| Statutory compliance | Applicable approved compliance documentation | MISSING |

The application analysis also identified OSHA, ISO 45001, and the Indian Factories Act as areas requiring appropriate compliance documentation.

Their mention does not establish that FactoryOps has completed or received certification for these standards.

---

## 9. Safety-Critical RAG Assistant Behavior

Safety-related questions must receive stricter handling than ordinary informational questions.

### Rule 1: Retrieve the correct SOP

Use the SOP ID, machine context, and relevant safety keywords to retrieve the appropriate procedure.

### Rule 2: Preserve exact safety values

Do not alter verified values such as:

- 6.0 bar
- 500–3000 RPM
- 8 minutes
- 0.003 mm
- 75%
- 0 bar
- 5 metric tons
- 415V
- 200°C
- 20 minutes
- 3 metres

### Rule 3: Do not invent missing procedures

If a user asks about a procedure that is not documented, explicitly state that the procedure is unavailable in the current FactoryOps knowledge base.

### Rule 4: Cite the source

Safety answers should identify their source SOP.

Examples:

- `[SOP-CNC-501 v3.2]`
- `[SOP-PRS-402 v2.8]`
- `[SOP-ROB-303 v4.0]`
- `[SOP-EMG-101 v5.1]`

### Rule 5: Do not treat incomplete documentation as authorization

A retrieved SOP does not establish that a user is authorized to perform the operation.

The assistant must respect FactoryOps role permissions.

### Rule 6: Escalate missing safety information

When the knowledge base does not contain the required safety procedure, the assistant must direct the user to the appropriate supervisor or authorized safety personnel rather than generating an assumed procedure.

### Rule 7: Keep safety instructions intact

During document chunking and retrieval, safety-critical steps and their warnings must remain together.

Do not split a safety instruction in a way that removes its associated precaution.

---

## 10. Recommended RAG Metadata

Each safety document should include metadata similar to:

```json
{
  "module": "safety",
  "document_type": "SOP",
  "safety_critical": true,
  "verification_status": "VERIFIED",
  "allowed_roles": [
    "SUPER_ADMIN",
    "ADMIN",
    "MANAGER_SUPERVISOR",
    "PRODUCTION_PLANNER",
    "TECHNICIAN"
  ]
}
```

The actual access scope must be aligned with FactoryOps authorization rules.

Recommended document metadata:

- SOP ID
- SOP title
- SOP version
- Machine or process category
- Safety-critical flag
- Verification status
- Effective date, when available
- Last updated date, when available

Do not invent effective dates or approval details.

---

## 11. Summary

FactoryOps currently contains four verified safety procedures:

1. SOP-CNC-501 — CNC Machine Operating Procedure.
2. SOP-PRS-402 — Hydraulic Press Operating Procedure.
3. SOP-ROB-303 — Robotic Welding Operating Procedure.
4. SOP-EMG-101 — Emergency Machine Shutdown Procedure.

These procedures cover selected operating requirements, machine precautions, LOTO-related requirements, PPE references, and emergency response.

However, the application does not contain a complete plant-wide safety manual.

The Advanced RAG assistant must preserve verified safety instructions, cite the relevant SOP, and clearly identify missing or unapproved safety information.

**Safety accuracy takes priority over generating a complete-sounding answer.**