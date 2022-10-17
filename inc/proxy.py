import os
import logging
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
        this.Copy(this.proxy, str(Path(this.buildPath).joinpath('build.json').resolve()))

        origConfig = this.executor.config
        origConfigArg = this.executor.parsedArgs.config
        this.executor.parsedArgs.config = this.proxy
        this.executor.PopulateConfig()
        this.executor.Build(None, ".", this.buildPath, this.events, **this.add_args)
        this.executor.config = origConfig
        this.executor.parsedArgs.config = origConfigArg

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
