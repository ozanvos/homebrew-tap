cask "monoprint" do
  version "0.1.4"
  sha256 "4fe312ea9b0ea9d6aa4a857035f71124a371b57d8b1cb450102109c8fdb058b7"

  url "https://github.com/ozanvos/monoprint/releases/download/v#{version}/Monoprint-#{version}-aarch64-apple-darwin.zip"
  name "Monoprint"
  desc "Create code images locally"
  homepage "https://monoprint.7ea.st/"

  livecheck do
    url :url
    strategy :github_latest
  end

  auto_updates true
  depends_on arch: :arm64
  depends_on macos: :monterey

  app "Monoprint.app"
  binary "#{appdir}/Monoprint.app/Contents/MacOS/monoprint"

  zap trash: [
    "~/Library/Application Support/Monoprint",
    "~/Library/Preferences/app.monoprint.studio.plist",
  ]
end
