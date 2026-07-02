class BitbucketManager < Formula
  include Language::Python::Virtualenv

  desc "TUI suite for managing Bitbucket Cloud from the terminal"
  homepage "https://github.com/AlanStefanov/bitbucket-manager"
  url "https://github.com/AlanStefanov/bitbucket-manager/archive/refs/tags/v0.4.2.tar.gz"
  sha256 "9f416fa948b80318e5b8d88d0a7f3d51a17ad6ee263c1d7b4522ab1feb6eeb31"
  license "MIT"

  depends_on "python@3.12"

  def install
    virtualenv_create(libexec, "python3.12")
    system libexec/"bin/pip", "install", buildpath
    bin.install_symlink libexec/"bin/bitbucket-manager"
  end

  test do
    assert_match "Bitbucket Manager", shell_output("#{bin}/bitbucket-manager --help")
  end
end
