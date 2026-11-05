cask "monoprint" do
  version "0.2.2"
  sha256 "21a85bd790e5b234e88cee564d987d2f79a6a82441f69e48797358702888ea8a"

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
