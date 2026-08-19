# FENCEGUARD-X Team Collaboration Guidelines

## 🤝 Our Team Commitment

**"From today, GitHub will be our single source of truth."**

Every task has:
- **Owner** (one person responsible)
- **Deadline** (specific date/time)
- **Status** (which column it's in)
- **Priority** (P0-P3)

---

## 📋 Daily Workflow

### Morning (Start of Day)
1. **9:50 AM**: Log into GitHub
2. **10:00 AM**: Standup meeting (10 minutes)
   - What did I complete yesterday?
   - What will I do today?
   - Am I blocked on anything?
3. **10:10 AM**: Go to project board
4. **10:15 AM**: Move your task card to "IN PROGRESS"

### Throughout the Day
- **Commit regularly** (every 30-60 min for big tasks)
- **Push to GitHub** (so others can see progress)
- **Add comments** if you find blockers
- **Help teammates** if they ask
- **Keep card updated** with progress

### End of Day
1. **5:50 PM**: Review your work
2. **6:00 PM**: (Optional) Evening sync if needed
3. **6:10 PM**: Update card status
   - If done: Move to REVIEW
   - If done but needs testing: Move to DONE
   - If blocked: Move to BLOCKED + add comment why
   - If continuing: Leave in IN PROGRESS

### Before Sleep
- **Push all code**
- **Update GitHub board**
- **Clear any BLOCKED cards** (assign next step)
- **Commit message should explain what was done**

---

## 📊 Card Status Explained

### BACKLOG
- Not yet assigned
- No clear deadline
- **Action**: Discuss in standup if you want to move to TODO

### TODO
- Assigned to someone
- Ready to start
- Has clear acceptance criteria
- **Action**: Start work → Move to IN PROGRESS

### IN PROGRESS
- You're actively working on it
- Code/design changes happening
- **Action**: Update daily, or move to BLOCKED/DONE

### REVIEW
- Work complete, needs approval
- Test complete, but waiting for code review
- **Action**: Ping reviewer with @mention, don't merge until approved

### DONE
- Merged into main branch
- Tested and verified working
- **Action**: None, it's finished!

### BLOCKED
- Can't proceed without something else
- Waiting for another task to finish
- Waiting on external input
- **Action**: Add comment explaining blocker + tag responsible person

---

## 🔄 How to Move Cards

### Moving FROM TO PROGRESS
```
1. You've finished coding
2. Add comment: "Implemented X, ready for testing"
3. Click "Convert to card" in PR or issue
4. Drag card to REVIEW column
5. @mention the reviewer
```

### Moving TO BLOCKED
```
1. You hit a problem
2. Add comment: "Blocked: waiting for hardware from Anup"
3. @mention @anup
4. Drag card to BLOCKED
5. Don't disappear - keep working on other things
```

### Moving FROM BLOCKED
```
1. Blocker is resolved
2. Add comment: "Unblocked! Hardware received"
3. Drag card back to IN PROGRESS
4. Continue work
```

---

## 💬 How to Comment

### Good Comment
```
✅ "Implemented sensor filtering. Results show false alarm rate < 2%. 
   Ready for firmware integration. @anup please review when ready."
```

### Bad Comment
```
❌ "done"
```

### Good Comment When Blocked
```
✅ "Can't proceed - waiting for ML model file from @priyada. 
   She said it'll be ready by 3 PM. I'll work on relay logic meanwhile."
```

### Good Comment for Help
```
✅ "@alok-kumar can you help debug MQTT connection? 
   Getting timeout error on line 234 of mqtt_handler.cpp. 
   Issue #42"
```

---

## 🔧 Git Workflow

### How to Commit
```bash
# After making changes
git status                    # See what changed
git add .                     # Stage changes
git commit -m "FW-02: Implement INA219 I2C driver

- Added I2C initialization at 100kHz
- Implemented current reading with ±1% accuracy
- Added calibration routine
- Tested with reference load"
git push                      # Send to GitHub
```

### Commit Message Format
```
[ISSUE-NUM]: Brief description

- What specifically changed
- Why you changed it
- Any notes for reviewers
```

### Examples
```
✅ Good:
FW-02: Implement INA219 I2C driver
- Initialized I2C0 at 100kHz on GPIO 21/22
- Implemented 16-bit conversion
- Tested accuracy ±1% range

❌ Bad:
fixed stuff
```

### When to Commit
- Every 30 minutes (at least)
- After completing a logical piece
- Before switching tasks
- Always before end of day

---

## 👥 Assigning Work

### To Assign an Issue to Yourself
1. Go to issue
2. Click "Assignee" on right side
3. Select your name
4. Add to project board if not already there

### To Ask Someone Else For Help
```
@anup can you review my MQTT code? Need your firmware expertise on line 45.
```

### To Hand Off to Someone
```
@priyada - ML model is ready. Can you integrate it into firmware? 
File is here: models/model_v1.tflite
Issue: #34
```

---

## 🎯 Priority Levels

### P0 (Critical)
- **If this doesn't work, the whole project fails**
- Deadline MUST be met
- Get help if stuck
- Work until it's done

**Examples**: ML inference on ESP32, relay isolation, backend API

### P1 (High)
- **Important for complete system**
- Can work around it if needed
- Can be deprioritized for P0 issues

**Examples**: Dashboard updates, error handling, documentation

### P2 (Medium)
- **Nice to have, improves polish**
- Can skip if time runs out
- Do after P0/P1

**Examples**: Fancy UI, optimization, extra features

### P3 (Low)
- **Only do if everything else is done**
- First thing to cut if time pressured

**Examples**: Comments, README polish

---

## ⏰ Deadline Format

### Example Deadlines
```
14-AUG 23:59  ← End of today
15-AUG 14:00  ← 2 PM tomorrow
16-AUG 18:00  ← 6 PM day after tomorrow
```

### How to Meet Deadlines
1. **Break into smaller steps**
   - Don't wait until 6 PM to start
   - Commit partial progress by lunch
   - Get feedback early

2. **Identify blockers early**
   - If you need something from someone else, ask NOW
   - Don't wait until deadline

3. **Have a backup plan**
   - Working 80% feature by deadline?
   - Better than 0% done at deadline
   - Can polish later

---

## 🆘 How to Ask for Help

### Problem: You're stuck
```
❌ Don't: Say nothing, waste 3 hours, then panic
✅ Do:    After 30 min stuck, ask in comments:

@anup quick question on line 45 of mqtt_handler.cpp
Getting "Connection timeout" on first connect attempt.
Debug output attached. Can you help debug?
```

### Problem: You need code review
```
❌ Don't: Push to main without review
✅ Do:    Push to branch, open PR, add comment:

@alok-kumar please review POST /api/v1/events endpoint
Implemented validation per spec, added error handling
Ready to merge after your approval
```

### Problem: Task is too hard
```
❌ Don't: Give up quietly
✅ Do:    Ask for pairing session:

@priyada - converting model to TFLite is harder than expected.
Available for 1-hour pairing session tomorrow 2 PM?
We can tackle it together.
```

---

## 🐛 Bug Reporting

### Found a Bug?
1. Create an issue with clear title
2. Add steps to reproduce
3. Add expected vs actual behavior
4. Assign to person who owns that module

**Example Issue Title:**
```
BUG: Relay stuck after isolation event (FW)
```

**Issue Body:**
```
1. Trigger critical event (simulate high current)
2. Relay cuts power (good)
3. Try to restore relay via reset button
4. Relay doesn't respond

Expected: Relay toggles back on
Actual: Relay stays off, no response
```

---

## 📈 Weekly Progress Check

**Every Friday (or Sunday if working weekends):**

1. Count issues in DONE column
2. Review BLOCKED column (resolve blockers)
3. Adjust deadlines if needed
4. Celebrate progress! 🎉

---

## 🤐 Confidentiality

This project is for SIH 2026. Keep it confidential until:
- Internal round is done
- You have permission to share
- You're making portfolio posts

---

## 🎮 Fun Ideas to Stay Motivated

### Celebrate Wins
- Move card to DONE → Celebrate in comments! 🎉
- First integration working → Post screenshot
- PPT slides completed → Share in team chat

### Friendly Competition
- Who can close the most issues by Friday?
- Shortest commit message? (must still explain work)
- Best documentation comment?

### Team Spirit
- Help someone get their first card to DONE
- Pair program on tricky issues
- Share knowledge in comments (teach/learn)

---

## ⚡ Emergency Procedures

### If Your Module Is Broken
1. **Assess damage** (1 min)
2. **Post in comments** (1 min)
   - Tag team lead
   - Explain what broke
   - Current status
3. **Move to BLOCKED** (1 min)
4. **Keep working on other stuff** (don't stop)
5. **Get help** (immediately)

**DON'T** silently disappear or wait for help without telling anyone

### If You'll Miss a Deadline
1. **Tell team ASAP** (same day at latest)
2. **Explain why** (technical issue? underestimated?)
3. **Show what you HAVE done**
4. **Ask for extension** or **help**
5. **Move card to BLOCKED**

---

## 📱 Response Times

**Expected Response Times:**

| Issue Type | Respond By |
|-----------|-----------|
| Question in GitHub | 1 hour |
| Tagged in issue | 30 min |
| Standup question | During standup |
| PR review request | Next working session |
| BLOCKED status | 30 min (to unblock) |
| Bug report | 1 hour |

---

## 🎓 Learning & Growth

While we build this project, you're also:
- Learning IoT systems
- Practicing agile/scrum
- Building leadership skills
- Collaborating on real product
- Creating portfolio project

**Be proud of your work!** This is professional-level project management.

---

## ✅ Checklist Before Going to Sleep

- [ ] All code pushed to GitHub
- [ ] Card status updated
- [ ] No BLOCKED cards sitting unassigned
- [ ] Commit messages clear and descriptive
- [ ] No uncommitted changes left in local repo
- [ ] Set alarm for tomorrow's standup 😴

---

## 🏁 Final Thoughts

**This isn't just about winning SIH.**

It's about:
- ✅ Building something real
- ✅ Learning to work as a team
- ✅ Shipping quality code
- ✅ Solving real problems
- ✅ Growing as engineers

**Your GitHub profile from this project will be impressive.**

Your ability to work in teams will set you apart.

Your portfolio will have a real project, not toy code.

---

**Let's build something amazing together.** 🚀

**See you at 10 AM for standup!**

---

**Last Updated**: 14 August 2026
**Made By**: FENCEGUARD-X Team
**Status**: 🟢 Ready to roll
