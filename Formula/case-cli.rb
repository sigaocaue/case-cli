# Homebrew formula for case-cli
#
# To publish this formula as a tap:
# 1. Create a repository named 'homebrew-case-cli' under your GitHub account
# 2. Place this file at Formula/case-cli.rb in that repository
# 3. Users can then install with:
#    brew tap sigaocaue/case-cli
#    brew install case-cli
#
# To update the formula after a new release:
# 1. Update the 'url' to point to the new release tarball
# 2. Update the 'sha256' checksum (run: shasum -a 256 <tarball>)
# 3. Update the 'version' if needed

class CaseCli < Formula
  include Language::Python::Virtualenv

  desc "Command-line tool for converting strings between case styles"
  homepage "https://github.com/sigaocaue/case-cli"
  url "https://files.pythonhosted.org/packages/source/c/case-cli/case-cli-0.1.0.tar.gz"
  sha256 "PLACEHOLDER_SHA256"
  license "MIT"

  depends_on "python@3"

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_equal "hello_world", shell_output("#{bin}/case-cli 'hello world' --case=snake").strip
  end
end
