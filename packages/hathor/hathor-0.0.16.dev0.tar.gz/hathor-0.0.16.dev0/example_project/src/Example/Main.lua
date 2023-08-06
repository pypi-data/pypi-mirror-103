---@entrypoint Script ServerScriptService.Server
local items = require("Core.ItemDB")

for _, item in pairs(items) do
    print(item.ID, item.Name)
end

print("Hello Roblox :D")
