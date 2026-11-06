cask "monoprint" do
  version "0.2.3"
  sha256 "ffd1922a93db21ca41bdfe8cb3fdff886f41f075c8948a83752f82a5a20b310d"

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
