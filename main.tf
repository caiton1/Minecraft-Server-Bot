provider "aws" {
    region = "us-west-1"
}

# variables
# allowing ssh port from anywhere, if more were at stake I would take a more secure approach
variable "openports"    {
    type = list(number)
    default = [25565,443,80,22] 
}

# provision ec2
resource "aws_instance" "minecraft_server"   {
    ami = "ami-059322e048360e2ed" # golden AWS linux AMI with java and minecraft installed
    instance_type = "t2.micro" 
    security_groups = [aws_security_group.minecraft_sg.name]
    tags = {
        Name = "Minecraft Server"
        server_name = "AZCRAFT"
        password = "N/A"
        discord_bot = "True"
        port = "25565"
        # attaching my personal key pair that I use for projects. You will have to change this for SSH
        key_name = "macbook" 
    }
    provisioner "local-exec" {
        # TODO: Fix
        command = "/bin/bash /home/ec2-user/start_server.sh"
    }
}

# security group, need 25565, SSH, HTTP and HTTPS 
resource "aws_security_group" "minecraft_sg" {
    name = "Minecraft TCP" 

    dynamic "ingress" {
        iterator = port
        for_each = var.openports
        content {
            from_port = port.value
            to_port = port.value
            protocol = "TCP"
            cidr_blocks = ["0.0.0.0/0"]
        }
        
    }

    dynamic "egress" {
        iterator = port
        for_each = var.openports
        content {
            from_port = port.value
            to_port = port.value
            protocol = "TCP"
            cidr_blocks = ["0.0.0.0/0"]
        }
    }
}

# outputs
output "minecraft_ip"   {
    value = aws_instance.minecraft_server.public_ip
}
output "minecraft_key"  {
    value = "key pair:${aws_instance.minecraft_server.key_name}"
}