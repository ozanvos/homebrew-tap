cask "monoprint" do
  version "0.2.4"
  sha256 "3d8b61eb5345004b34b40b20d358f351ad931a5234322429dd1726059668cb2e"

  url "https://github.com/ozanvos/monoprint/releases/download/v#{version}/Monoprint-#{version}-aarch64-apple-darwin.dmg"
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
