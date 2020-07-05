# Electron Dilemma

Yes I know, it is currently using Electron. When I was getting into frontend development, I saw Electron as that shiny swiss-army knife that has the right tools for me to develop cross-platform apps using web technologies. It didn't take long enough for me to realize that the swiss-army knife itself already weighs a few kilograms.

I had this question out of naivety. Can I call it a tradeoff if TridentFrame's large application file size is offset by putting a lot of features to it? Of course not. Electron seem suitable for large scale applications, and TridentFrame was never designed to provide complex features. A resource-eating core of a browser (Chromium) living inside it seem like an overkill.

Yes I am considering alternatives to Electron like Qt5, NW.js, Proton Native, Vuido and NodeGUI (or Vue-NodeGUI). However,

- **Qt5** fell short as I do not want to rewrite the entire HTML-CSS-JS frontend into Qt's python GUI Framework.
- **NW.js** also ships with Chromium inside it so there is little difference to Electron in regards to reducing bloat.
- **Proton Native** currently only works for React-based projects while TridentFrame is built using Vue.
- **Vuido** does not provide styling based on HTML-CSS and only allows native platform GUI, it was never meant to be built for it.
- **NodeGUI**, which is based on `Qt5`, is slightly better for supporting at least the rewrite in `javascript` for familiarity, although styling will need testing on it to see how it goes.
- **Vue-NodeGUI**, which is based on `NodeGUI`, has an even better support for already existing projects using `.vue` files, and handles translation of CSS `<styles>` in Vue into Qt5's `Window.styleSheet`.

Out of these 6, `Vue-NodeGUI` is my best candidate. However, the `NodeGUI` project is still in its infancy, and `Vue-NodeGUI` is currently in work-in-progress status and still has a lot of core features needed to be finished compared to a similar abstraction for React (`React-NodeGUI`).

As of this time of commit, I am waiting and keeping an eye on how well both `NodeGUI` and `Vue-NodeGUI` develops over time.
