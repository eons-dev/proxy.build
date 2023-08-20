import os
import logging
import eons
from pathlib import Path
from ebbs import Builder

# Class name is what is used at cli, so we defy convention here in favor of ease-of-use.
class proxy(Builder):
    def __init__(this, name="Test"):
        super().__init__(name)

        this.clearBuildPath = False

        this.requiredKWArgs.append("proxy") #what to proxy

        this.optionalKWArgs["add_args"] = {} #any extra args

        this.supportedProjectTypes = []

    # Required Builder method. See that class for details.
    def DidBuildSucceed(this):
        return True  # TODO: how would we even know?

    # Required Builder method. See that class for details.
    def Build(this):
        # events = this.events
        # events.add("proxied")
        # eventStr = ""
        # for e in events:
        #    eventStr += f" --event {e}"

        for arg, mem in this.configNameOverrides.items():
            if (arg not in this.add_args):
                this.add_args[arg] = getattr(this, mem)
        this.add_args['precursor'] = this

        this.proxy = str(Path(this.rootPath).joinpath(this.proxy).resolve())

        this.proxyFile = "build."+this.proxy.split('/')[-1].split('.')[-1]
        this.Copy(this.proxy, str(Path(this.buildPath).joinpath(this.proxyFile).resolve()))

        orig = eons.util.DotDict()
        orig.args = this.executor.extraArgs
        orig.config = this.executor.config
        orig.configArg = this.executor.parsedArgs.config
        orig.builder = this.executor.parsedArgs.builder
        orig.path = this.executor.rootPath
        orig.buildIn = this.executor.default.build.directory
        orig.events = this.executor.events
        orig.next = this.executor.next

        this.executor.parsedArgs.config = this.proxy
        this.executor.parsedArgs.builder = None
        this.executor.PopulateConfig()
        this.executor.rootPath = "."
        this.executor.default.build.directory = this.buildPath
        this.executor.events = this.events
        this.executor.next = []
        this.executor.extraArgs = this.add_args
        # this.executor.Build(None, ".", this.buildPath, this.events, **this.add_args)
        this.executor()
        
        this.executor.extraArgs = orig.args
        this.executor.config = orig.config
        this.executor.parsedArgs.config = orig.configArg
        this.executor.parsedArgs.builder = orig.builder
        this.executor.rootPath = orig.path
        this.executor.default.build.directory = orig.buildIn
        this.executor.events = orig.events
        this.executor.next = orig.next

        #        this.RunCommand(f'''ebbs        \
        # {' -q' * this.executor.parsedArgs.quiet}     \
        # {' -v' * this.executor.parsedArgs.verbose}     \
        # -c {this.proxy}                         \
        # --name {this.projectName}             \
        # --type {this.projectType}             \
        # --clear_build_path {this.clearBuildPath} \
        # --build_in {this.buildPath}             \
        # {eventStr}                               \
        # {' '.join(this.add_args)}             \
        # ''')
