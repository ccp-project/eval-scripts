Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/artful64"
  config.vm.post_up_message = ""\
    "Welcome to CCP. "\
    "Run `make build` in /ccp to compile. This may take some time. "\
    "Add your own congestion control algorithm in `your_code`, and modify `scripts/algs.py` to run it"
  config.vm.synced_folder ".", "/ccp"
  config.vm.provision "shell", path: "ccp-system-setup.sh"
end
