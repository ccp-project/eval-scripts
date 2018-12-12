Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.post_up_message = ""\
    "Welcome to CCP. "\
    "Run `make` in /ccp to compile. This may take some time. "
  config.vm.synced_folder ".", "/ccp"
  config.vm.provision "shell", path: "ccp-system-setup.sh"
end
