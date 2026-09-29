-- figure-alt.lua: give each figure separate alt text and caption in DOCX.
-- scripts/render_diagrams.py writes
--   ![Figure N — caption](_figures/x.png){width=6.25in fig-alt="alt text"}
-- Pandoc uses the bracketed text as the caption; this filter moves the
-- fig-alt attribute into the image description, so Word's alt text (docPr
-- descr) carries the alt text and the caption stays below the figure.
function Image(img)
  local alt = img.attributes["fig-alt"]
  if alt then
    img.caption = pandoc.Inlines(pandoc.Str(alt))
    img.attributes["fig-alt"] = nil
  end
  return img
end
