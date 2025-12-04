This doc contains 3 separate plans by agents without context for corelink expansions. Analyze with meta-awareness, clarify end product goal with user \- critique each agents plan because they didn’t have full context when they were making it. Simulate how it will work at the end, try to find holes, ask clarifying questions. It’s imperative that we uncover potential faults before we start to implement.The 3 things are \- python chat log grabber (playwright? I forget the name), chat log processer/parser, UI launcher for different PWAs/gmail accounts.

\[M:ROLE\_CLARIFICATION|SCOPE=WHAT\_NOT\_HOW|DELIVERABLE=FACTS\_AND\_GOALS\_ONLY|NO\_CODE=TRUE|NO\_IMPLEMENTATION=TRUE|NO\_ASSUMPTIONS=TRUE|FORMAT=DOT\_POINTS\]

\---

\*\*Human Section: Pure Facts & Goals Specification\*\*

\*\*For Next Agent: CoreLink PWA Launcher Integration\*\*

\---

\#\# \*\*1. ENVIRONMENT FACTS\*\*

\- \*\*OS\*\*: Windows 11 laptop, 4GB RAM  
\- \*\*Default Browser\*\*: Brave (registry: BraveHTML)  
\- \*\*Chrome\*\*: Anime-only, sacred space, never touched by work  
\- \*\*Brave\*\*: Handles external links from PWAs \+ disposable browsing  
\- \*\*Taskbar-only\*\*: No Start Menu usage

\---

\#\# \*\*2. CURRENT APPLICATION STATE\*\*

\- \*\*Kimi AI\*\*: PowerShell script → Brave, 1 Gmail account (to be replaced)  
\- \*\*ChatGPT\*\*: PowerShell script → Brave, 1 Gmail account (to be replaced)  
\- \*\*Grammarly\*\*: Native Edge PWA, 1 Gmail account (keep, need to inspect)  
\- \*\*ASCII Flow\*\*: Native Edge PWA, 1 Gmail account (keep, need to inspect)  
\- \*\*Google Drive (browser workstation)\*\*: No working version exists  
\- \*\*Google Drive File Stream\*\*: Desktop sync app (irrelevant to this project)

\---

\#\# \*\*3. EDGE PROFILE EXPLORATION NEEDED\*\*

Run these commands before design:  
\`\`\`powershell  
\# 1\. Identify all Edge profiles and their names  
Get-ChildItem "$env:LOCALAPPDATA\\Microsoft\\Edge\\User Data" \-Directory | Where-Object { $\_.Name \-match '^(Default|Profile \\d+)$' } | ForEach-Object { $prefs="$($\_.FullName)\\Preferences"; $name="Unnamed"; if(Test-Path $prefs){ try{ $name=(Get-Content $prefs|ConvertFrom-Json).profile.name }catch{} }; "Profile: $($\_.Name) | Name: $name" }

\# 2\. Extract all Edge PWA app IDs and their profiles  
Get-ChildItem "$env:LOCALAPPDATA\\Microsoft\\Edge\\User Data\\\*\\Web Applications\\\*\\manifest.json" | ForEach-Object { $m=Get-Content $\_ \-Raw|ConvertFrom-Json; $profile=(Split-Path $\_ \-Parent).Split('\\')\[-3\]; "$($m.name) | Profile: $profile | App ID: $($m.app\_launcher\_id)" }  
\`\`\`

\*\*Questions to answer:\*\*  
\- Which profile contains Grammarly PWA?  
\- Which Gmail is Grammarly signed into?  
\- Which profile contains ASCII Flow PWA?  
\- What is Edge "Profile 2" used for?

\---

\#\# \*\*4. DECISIONS (LOCKED)\*\*

\- Create \*\*two new Edge profiles\*\* for Gmail accounts (names pending user specification)  
\- Install \*\*fresh native PWAs\*\* in Edge (abandon PowerShell scripts)  
\- All PWAs must open links in \*\*Brave\*\* (not Edge)  
\- Google Drive must open Docs/Sheets as \*\*tabs within same window\*\*  
\- \*\*Minimize memory\*\* (single Edge engine, no redundant processes)  
\- CoreLink gets new button: "Launch Apps" (opens separate window)  
\- Launcher backend uses simple app-to-profile mapping  
\- Design must support future 2nd ChatGPT account and potential 2nd Grammarly account

\---

\#\# \*\*5. BEHAVIORAL REQUIREMENTS\*\*

\*\*Google Drive Workstation:\*\*  
\- Must support in-window account switching via Google UI  
\- Must trap Docs/Sheets as internal tabs  
\- \*\*Fallback\*\*: If in-window switching fails, implement dual separate app icons

\*\*Link Redirection:\*\*  
\- URL clicks in any Edge PWA → must open in Brave  
\- No leakage to Edge main browser  
\- No interference with Chrome or Brave normal operation

\*\*App Independence:\*\*  
\- Each app launches in its own window  
\- No cross-contamination between apps or accounts

\*\*Memory:\*\*  
\- Target: As low as possible given 4GB constraint  
\- Disable sync, extensions in PWA profiles

\---

\#\# \*\*6. CRITICAL QUESTIONS FOR USER\*\*

Before implementation, next agent must ask:

1\. \*\*Gmail profile naming\*\*: What should the two new profiles be called? (\`Gmail1/Gmail2\`? \`Work/Personal\`?)

2\. \*\*Grammarly placement\*\*: Which Gmail account should Grammarly be associated with? Or should it stay in its current profile?

3\. \*\*Current profile usage\*\*: What is Edge "Profile 2" currently used for? Should it be repurposed or kept separate?

4\. \*\*Google Drive test\*\*: The user has a broken Brave PWA. They need to test if Edge \`--app\` mode maintains tab behavior. Provide test command and ask for results.

\---

\#\# \*\*7. GOALS\*\*

\#\#\# \*\*Primary Goals\*\*  
\- Consolidate all PWAs into Edge (reduce memory from 3 browsers to 1\)  
\- Achieve proper account isolation between Gmail accounts  
\- Enable in-window Google Drive tab behavior  
\- Ensure all PWA links open in Brave  
\- Integrate launcher into CoreLink without breaking existing queue functionality

\#\#\# \*\*Secondary Goals\*\*  
\- Support future addition of 2nd ChatGPT account  
\- Support future addition of 2nd Grammarly account  
\- Maintain scalability for new apps  
\- Keep implementation modular and maintainable

\---

\#\# \*\*8. EXPLICITLY OUT OF SCOPE\*\*

\- \*\*UI Design\*\*: Launcher layout, button aesthetics, window size (user will customize)  
\- \*\*Implementation Code\*\*: Next agent writes all code with full context  
\- \*\*Error Handling Strategy\*\*: Next agent determines appropriate try/catch patterns  
\- \*\*Performance Flags\*\*: Next agent evaluates if any flags are needed (but default to none)  
\- \*\*Specific Memory Target\*\*: "Minimize" is sufficient, no numeric target

\---

\*\*End of Specification. No code. No implementation details. Only facts and goals.\*\*  
