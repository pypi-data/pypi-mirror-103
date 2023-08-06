# Pytrika

[![N|Solid](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Echo_pagelinked.svg/96px-Echo_pagelinked.svg.png)]()

Pytrika allows you to document web urls related to your project. If certain posts on stackoverflow or blog-posts or even videos helped you during the development of your project you can document them in your project using Pytrika.

# What's the need?

  + To help other developers get extra-insight on the resource/approach utlizied in the project.
  + It serves as a pointer to the accurate resources.

        There are many resources that pertain to a macro level problem, with many possible solutions. 
        You can help people point to the exact resource out of all the resources that worked for you during the development of the project.

# Give me an example.

Let us say you are working on a project called TEST. While woring on TEST, you run into some errors. While some errors might be easy to fix, some errors are time-consuming. You have to go through multiple stackoverflow questions and other online resources to find the resource that best suits your needs in the current project. Once you find "the one" solution that helped you, you would love to let others know especially the ones working on the same project, where you were able to find the solution and point them to that exact resource and help them save time from skimming through other irrelevant resources that revolve around the same topic.

# Can't this be done in the wiki or README already?

+ It can be done. I just find it more convenient to use this Pytrika instead.

# How do I use it?
+ Create a bookmark directory in your browser (currently, only Firefox, Chrome
  and Chrome Canary are supported) with the exact name as you project root.
        - If you are working at `path/to/MyProject` , create a bookmark directory called `MyProject` in your browser.
        - Just bookmark the resources in the `MyProject` directory in your browser.

# Is git branch supported?
+ Yes, only with Chrome as of now. If you are working with a git branch, you should follow the namespace
  while bookmarking your resource as repo_name::branch_name. Example:
  Pytrika::master. You then pass the flags `-g True`. Example: `cthis -g True`.
  For Chrome Canary, you can use the flags as such `cthis -flv canary`.
