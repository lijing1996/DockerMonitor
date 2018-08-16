# Welcome to AI cluster
### Cluster Information
This cluster contains one admin nodes and 18 computing nodes named nodeXX (XX ranges from 01 to 18) with NVIDIA GPUs. This cluster is mean to serve for large scale parallel float computing using NVIDIA GPU, which is very common in Machine Learning, especially Deep Learning research and applications. CentOS is the base opearating system for all computers in AI cluster, however, since we use chroot to protect the base OS, all users will chroot into an Ubuntu 16.04 sandbox operating system after login.

The following pages will guide you through the setup and introduce you to the very basics of working with cluster and rules you should follow when using AI cluster.

Before further reading, please **Keep in mind**:

```Cluster is NOT your personal computer. Instead, it’s computing resources for all of us!```

In order to keep our cluster ready for use for all of us at anytime, you are restrict to do something that you may do everyday on your personal computer. However, as you will see in this doc, all these restrictions should NOT limit your work, as long as you change your usage habits a bit and understand basics of linux operating system.

Wish all of you have fun during working with AI cluster!

### Acknowledgements
If you have any problem, we strongly recommend you first try to search your problem using google or any other search engine you like, their may (perhaps always) exists some awosome solutions to help you and you will definitely learn a lot when solving your problems yourself. However, you can feel free to ask us cluster administrators for help if necessary.