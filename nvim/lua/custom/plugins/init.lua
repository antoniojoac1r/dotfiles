return {
  {
    'norcalli/nvim-colorizer.lua',
    opts = {
      'css',
    },
  },
  {
    'saghen/blink.cmp',
    dependencies = 'rafamadriz/friendly-snippets',
    version = '*',
    opts = {
      keymap = { preset = 'default' },
      appearance = {
        use_nvim_cmp_as_default = true,
        nerd_font_variant = 'mono',
      },
      signature = { enabled = true },
    },
  },
  {
    -- https://github.com/mfussenegger/nvim-jdtls
    'mfussenegger/nvim-jdtls',
    ft = 'java',
  },
}
