return {
    {
        "bjarneo/aether.nvim",
        branch = "v3",
        name = "aether",
        priority = 1000,
        opts = {
            transparent = false,
            colors = {
                -- Background colors
                bg = "#0b1d20",
                bg_dark = "#030e10",
                bg_highlight = "#1e4147",

                -- Foreground colors
                -- fg: Object properties, builtin types, builtin variables, member access, default text
                fg = "#94b3b5",
                -- fg_dark: Inactive elements, statusline, secondary text
                fg_dark = "#82a3a6",
                -- comment: Readable comments and secondary syntax
                comment = "#719398",

                -- Accent colors
                -- red: Errors, diagnostics, tags, deletions, breakpoints
                red = "#ed634c",
                -- orange: Constants, numbers, current line number, git modifications
                orange = "#d07a3f",
                -- yellow: Types, classes, constructors, warnings, numbers, booleans
                yellow = "#b79a54",
                -- green: Comments, strings, success states, git additions
                green = "#58ad73",
                -- cyan: Parameters, regex, preprocessor, hints, properties
                cyan = "#00c6c2",
                -- blue: Functions, keywords, directories, links, info diagnostics
                blue = "#668ca9",
                -- purple: Storage keywords, special keywords, identifiers, namespaces
                purple = "#9c8499",
                -- magenta: Function declarations, exception handling, tags
                magenta = "#9c8499",
            },
        },
        config = function(_, opts)
            require("aether").setup(opts)
            vim.cmd.colorscheme("aether")

            -- Enable hot reload
            require("aether.hotreload").setup()
        end,
    },
    {
        "LazyVim/LazyVim",
        opts = {
            colorscheme = "aether",
        },
    },
}
