<!--





 -->

Core Features (MVP)

Implement markdown
User accounts (login/signup).
Notes CRUD (create, edit, delete, archive).
Tagging system (multiple tags per note).
Search & filter (by tag, keyword).
Rich text editing (bold, lists, images).
Pinning & favorites.
Drag-and-drop UI (e.g., reorder notes, drag tags)
Version history (keep old versions of notes)
Offline mode + sync (use local storage/IndexedDB + backend sync).
Collaboration (share a note with another user, even real-time w/ WebSockets).
Export/import (PDF, markdown, etc).

Your users should be able to:

Create, read, update, and delete notes
Archive notes
View all their notes
View all archived notes
View notes with specific tags
Search notes by title, tag, and content
Select their color theme
Select their font theme
Receive validation messages if required form fields aren't completed
Navigate the whole app and perform all actions using only their keyboard
View the optimal layout for the interface depending on their device's screen size
See hover and focus states for all interactive elements on the page
Bonus: Save details to a database (build the project as a full-stack app)
Bonus: Create an account, log in, change password (add user authentication to the full-stack app)
Bonus: Reset their password (add password reset to the full-stack app)

💡
Ideas to test yourself
Add a WYSIWYG editor with text formatting for the notes
Use animations and transitions to add a layer of polish to the application
Build the project out as a full-stack application
Add user authentication (if building it as a full-stack app)
Add password reset capabilities

Progress update

For the past few months, I’ve been chasing that “perfect” idea for my CS50 Web final project. Eventually, inspiration struck: a note-taking app. Cliche? Yeah🙄. Simple? Yeah🙄. Until I decided to torture myself by implementing Google OAuth 😭. Honestly, who sent me?

I spent the past week wrestling with authentication. Imagine this: me, React on the frontend, Django on the backend, and Google OAuth standing in the corner, laughing at my pain. Looking back, picking React for this was like bringing a bazooka to a chess game — impressive, but completely unnecessary.

Still, I pushed through. I wrote the entire frontend in React, then hit the OAuth stage. After hopping from one YouTube video to another, I actually got sign-in working 🎉. But then came the dreaded CORS problem: backend holding the cookies, frontend unable to touch them, and I was stuck in developer limbo — like being at a party where the snacks are in the kitchen, but someone locked the door. Basically… cookies I couldn’t eat 🍪💔.

I reached out to friends and other devs for help (big thanks 🙏🏽). Their advice was super useful, and the breakthrough came when I finally switched back to Django’s default templates—like running home after realizing fast food can’t beat mom’s cooking. Along the way, I picked up lessons and concepts I didn’t even know I was missing.

At the end of the day, the biggest lesson was this: sometimes the stack you think will make life easier is the same stack that trips you up. As the saying goes, “Smooth seas never made a skilled sailor.”

Next stage: I need to wrap up the project, submit it, and then wait for the CS50 team to manually review it. Wish me luck👍. If you’ve ever had your own OAuth/CORS horror story, I’d love to hear it!

#CS50 #WebDevelopment #Django #React #OAuth #Python #Programming #LearnByBuilding
