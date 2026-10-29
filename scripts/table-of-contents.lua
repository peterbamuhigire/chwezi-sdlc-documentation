-- Emit a populated, navigable contents list. Pandoc's default --toc field is
-- deferred to Word/LibreOffice and can appear blank until the file is opened.
function Pandoc(doc)
  local items = {}
  for _, block in ipairs(doc.blocks) do
    if block.t == "Header" and block.level <= 3 then
      local title = pandoc.utils.stringify(block.content)
      if title ~= "Contents" and block.identifier ~= "" then
        local link = pandoc.Link(block.content, "#" .. block.identifier)
        local para = pandoc.Para(link)
        table.insert(items, {para})
      end
    end
  end

  if #items == 0 then
    return doc
  end

  local toc = {
    pandoc.Header(2, {pandoc.Str("Contents")}),
    pandoc.BulletList(items),
  }
  local blocks = pandoc.List(toc)
  for _, block in ipairs(doc.blocks) do
    blocks:insert(block)
  end
  doc.blocks = blocks
  return doc
end
