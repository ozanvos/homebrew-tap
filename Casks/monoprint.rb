cask "monoprint" do
  version "0.1.1"
  sha256 "4e3f5d0268bceaa434caeb9e318d9e66c057350b992fce4c95e8d0441f731f19"

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
