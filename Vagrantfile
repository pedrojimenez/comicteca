# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.box = "debian/jessie64"
  config.vm.hostname = "comicteca-dev"

  config.vm.provision :file, source: '~/.gitconfig',
    destination: '/home/vagrant/.gitconfig' if File.exist?(ENV['HOME'] +
                                                           '/.gitconfig')
  config.vm.provision :file, source: '~/.ssh/id_rsa',
    destination: '/home/vagrant/.ssh/id_rsa' if File.exist?(ENV['HOME'] +
                                                            '/.ssh/id_rsa')

  server_ip = "192.168.44.44"
  cpus = 2

  config.vm.provision "shell" do |s|
    s.path = "bootstrap.sh"
    s.args = [server_ip, cpus]
  end

  config.vm.provider "virtualbox" do |v|
    v.name = "Comicteca (dev)"
    v.memory = 1024
    v.cpus = cpus
  end

  config.vm.network :private_network, ip: server_ip
  config.vm.network "forwarded_port", guest: 80, host: 8080

  comicteca_dumps_path = "../dumps_comicteca"
  config.vm.synced_folder ".", "/vagrant",
    type: "rsync", rsync__exclude: ".git/"
  config.vm.synced_folder comicteca_dumps_path, "/home/vagrant/dumps_comicteca",
    type: "rsync", rsync__exclude: ".git/"

 if Vagrant.has_plugin?("vagrant-proxyconf")
    config.proxy.http     = ""
    config.proxy.https    = ""
    config.proxy.no_proxy = "localhost,127.0.0.1,*"
  end

end
