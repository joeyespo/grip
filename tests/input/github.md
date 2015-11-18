GitHub Flavored Markdown Test
=============================

This Markdown file contains all the features of **GitHub Flavored Markdown** for
testing a renderer with.

The features are taken directly from [Daring Fireball](https://daringfireball.net/projects/markdown/syntax)
and [GitHub Flavored Markdown](https://help.github.com/articles/github-flavored-markdown/),
followed by a list of one-offs.


Inline HTML
-----------

<table>
  <tr>
    <td>Foo</td>
  </tr>
  <tr>
    <td>
      Note that Markdown formatting syntax is not processed within block-level HTML tags.
      E.g., you can’t use Markdown-style *emphasis* inside an HTML block.
    </td>
  </tr>
</table>

Span-level HTML tags — e.g. &lt;span&gt;, &lt;cite&gt;, or &lt;del&gt; — can be used anywhere
in a Markdown paragraph, list item, or header. If you want, you can even use HTML tags instead
of Markdown formatting; e.g. if you’d prefer to use HTML &lt;a&gt; or &lt;img&gt; tags instead
of Markdown’s link or image syntax, go right ahead.

#### Testing <span>span</span>, <cite>cite</cite>, and <del>del</del> tags

Testing <span>span</span>, <cite>cite</cite>, and <del>del</del> tags in a paragraph.

And each element in its own list item:
- <span>This is within a span tag.</span>
- <cite>This is within a cite tag.</cite>
- <del>This is within a del tag.</del>


Automatic escaping for special characters
-----------------------------------------

- &copy; copyright
- AT&T should render the same as AT&amp;T
- 4 < 5 should render the same as 4 &lt; 5

Note that GitHub Flavored Markdown has URL autolinking, which will *not*
convert `&amp;`. So these two should yield different links:

- http://images.google.com/images?num=30&q=larry+bird
- http://images.google.com/images?num=30&amp;q=larry+bird


Paragraphs and line breaks
--------------------------

This is a normal paragraph.

This and the next sentence is separated by a single newline.
This should be on the same line.

This and the next sentence is joined by a single `<br />`. <br />
This should be on a new line, directly below.

These two sentences are separated by two `<br />` tags. <br /><br />
This should be two lines below.

These two paragraphs are separated by two `<br />` tags. <br /><br />

This should be three lines below.


Headers
-------

Here are some headers followed by [Lorem Ipsum](https://en.wikipedia.org/wiki/Lorem_ipsum).


This is an H1 (Setext-style)
============================

Lorem ipsum dolor sit amet, consectetur adipiscing elit.


This is an H2 (Setext-style)
----------------------------

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

The following are atx-style.


# This is an H1

Lorem ipsum dolor sit amet, consectetur adipiscing elit.


## This is an H2

Mauris feugiat, augue vitae sollicitudin vulputate, neque arcu dapibus eros, eget semper lorem ex rhoncus nulla.


### This is an H3

Etiam sit amet orci sit amet dui mollis molestie.


#### This is an H4

Cras et elit egestas, lacinia est eu, vestibulum enim.


##### This is an H5

Phasellus sed suscipit quam.


###### This is an H√36

Nam rutrum imperdiet purus, sit amet porttitor augue tempor quis.


Blockquotes
-----------

Email-style blockquotes:

> This is a blockquote with two paragraphs. Lorem ipsum dolor sit amet,
> consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus.
> Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.
>
> Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse
> id sem consectetuer libero luctus adipiscing.

Putting the > before the first line of a hard-wrapped paragraph:

> This is a blockquote with two paragraphs. Lorem ipsum dolor sit amet,
consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus.
Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.

> Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse
id sem consectetuer libero luctus adipiscing.

Nested blockquotes (i.e. a blockquote-in-a-blockquote):

> This is the first level of quoting.
>
> > This is nested blockquote.
>
> Back to the first level.

Blockquotes containing other Markdown elements:

> ## This is a header.
>
> 1.   This is the first list item.
> 2.   This is the second list item.
>
> Here's some example code:
>
>     return shell_exec("echo $input | $markdown_script");


Lists
-----

##### These three lists should be equivalent

First:

*   Red
*   Green
*   Blue

Second:

+   Red
+   Green
+   Blue

Third:

-   Red
-   Green
-   Blue


#### These three ordered lists should be equivalent

First:

1.  Bird
2.  McHale
3.  Parish

Second:

1.  Bird
1.  McHale
1.  Parish

Third:

3. Bird
1. McHale
8. Parish


#### These two lists should be equivalent

First:

*   Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
    Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi,
    viverra nec, fringilla in, laoreet vitae, risus.
*   Donec sit amet nisl. Aliquam semper ipsum sit amet velit.
    Suspendisse id sem consectetuer libero luctus adipiscing.

Second:

*   Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi,
viverra nec, fringilla in, laoreet vitae, risus.
*   Donec sit amet nisl. Aliquam semper ipsum sit amet velit.
Suspendisse id sem consectetuer libero luctus adipiscing.


#### Paragraphs and lists

*   Bird
*   Magic

Blank line separated:

*   Bird

*   Magic


#### Paragraphs within lists

First:

1.  This is a list item with two paragraphs. Lorem ipsum dolor
    sit amet, consectetuer adipiscing elit. Aliquam hendrerit
    mi posuere lectus.

    Vestibulum enim wisi, viverra nec, fringilla in, laoreet
    vitae, risus. Donec sit amet nisl. Aliquam semper ipsum
    sit amet velit.

2.  Suspendisse id sem consectetuer libero luctus adipiscing.

Second:

*   This is a list item with two paragraphs.

    This is the second paragraph in the list item. You're
only required to indent the first line. Lorem ipsum dolor
sit amet, consectetuer adipiscing elit.

*   Another item in the same list.


#### Blockquote within a list

*   A list item with a blockquote:

    > This is a blockquote
    > inside a list item.


#### Code within a list

*   A list item with a code block:

        <code goes here>


#### Accidental lists

1986. What a great season. (oops, I wanted a year, not a list)

1986\. What a great season. (*whew!* there we go)


Code blocks
-----------

This is a normal paragraph:

    This is a code block.


Here is an example of AppleScript:

    tell application "Foo"
        beep
    end tell

Markdown will handle the hassle of encoding the ampersands and angle brackets:

    <div class="footer">
        &copy; 2004 Foo Corporation
    </div>


    def this_is
      puts "some #{4-space-indent} code"
    end

<code>
print('Code block')
</code>

<pre>
print('Pre block')
</pre>


Horizontal rules
----------------

* * *

***

*****

- - -

---------------------------------------


Links
-----

Markdown supports two style of links: inline and reference.

This is [an example](http://joeyespo.com/ "Title") inline link.

[This link](http://joeyespo.com/) has no title attribute.

See my [About](/about/) page for some awesome people (*note: broken link*).

This is [an example][id] reference-style link.
This is [an example] [id] reference-style link with a space separating the brackets.

These should all be equivalent:

- [foo 1][]
- [foo 2][]
- [foo 3][]
- [foo 4][]
- [foo 5][FOO 5]


[id]: http://joeyespo.com/  "Optional Title Here"
[foo 1]: http://joeyespo.com/  "Optional Title Here"
[foo 2]: http://joeyespo.com/  'Optional Title Here'
[foo 3]: http://joeyespo.com/  (Optional Title Here)
[foo 4]: <http://joeyespo.com/>  "Optional Title Here"
[foo 5]: http://joeyespo.com/
    "Optional Title Here"


Emphasis
--------

- *single asterisks*
- _single underscores_
- **double asterisks**
- __double underscores__
- un*frigging*believable
- \*this text is surrounded by literal asterisks\*


Code
----

- Use the `printf()` function.
- ``There is a literal backtick (`) here.``
- A single backtick in a code span: `` ` ``
- A backtick-delimited string in a code span: `` `foo` ``
- Please don't use any `<blink>` tags.
- `&#8212;` is the decimal-encoded equivalent of `&mdash;`


Images
------

- ![Alt text](https://raw.githubusercontent.com/joeyespo/grip/master/artwork/favicon.ico)
- ![Alt text](https://raw.githubusercontent.com/joeyespo/grip/master/artwork/favicon.ico "Optional title")
- ![Alt text][img]
- <img src="https://raw.githubusercontent.com/joeyespo/grip/master/artwork/favicon.ico" width="32" height="32" /> &nbsp; &larr; bigger &amp; blurrier


[img]: https://raw.githubusercontent.com/joeyespo/grip/master/artwork/favicon.ico   "Optional title attribute"


Automatic links
---------------

- <http://joeyespo.com/>
- <joe@joeyespo.com>


Backslash escapes
-----------------

- \*literal asterisks\*
- \\   backslash
- \`   backtick
- \*   asterisk
- \_   underscore
- \{\}  curly braces
- \[\]  square brackets
- \(\)  parentheses
- \#   hash mark
- \+   plus sign
- \-   minus sign (hyphen)
- \.   dot
- \!   exclamation mark


GitHub Flavored Markdown
------------------------

See [GitHub Flavored Markdown](https://help.github.com/articles/github-flavored-markdown/) for details.

#### Multiple underscores in words

- wow_great_stuff


#### URL autolinking

http://joeyespo.com


#### Strikethrough

~~Mistaken text.~~


#### Fenced code blocks

```
function test() {
  console.log("notice the blank line before this function?");
}
```


#### Syntax highlighting

```python
print('Hello!')
```

```javascript
console.log('JavaScript!');
```

```js
console.log('JavaScript (with js)!');
```

```unmatched_language
console.log('No matching language, but looks like JavaScript.');
```


#### Tables

Simple:

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell

Pipes:

| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |

Unmatched:

| Name | Description          |
| ------------- | ----------- |
| Help      | Display the help window.|
| Close     | Closes a window     |

Inner Markdown:

| Name | Description          |
| ------------- | ----------- |
| Help      | ~~Display the~~ help window.|
| Close     | _Closes_ a window     |

Alignment:

| Left-Aligned  | Center Aligned  | Right Aligned |
| :------------ |:---------------:| -----:|
| col 3 is      | some wordy text | $1600 |
| col 2 is      | centered        |   $12 |
| zebra stripes | are neat        |    $1 |
Text right below a table.


#### HTML

*TODO: Test all allowed HTML tags.*


Writing on GitHub
-----------------

See [this article](https://help.github.com/articles/writing-on-github/) for details.


####  Newlines

Roses are red
Violets are Blue


#### Task lists

- [x] @mentions, #refs, [links](), **formatting**, and <del>tags</del> are supported
- [x] list syntax is required (any unordered or ordered list supported)
- [x] this is a complete item
- [ ] this is an incomplete item

Task lists can be nested to better structure your tasks:

- [ ] a bigger project
  - [x] first subtask #1234
  - [ ] follow up subtask #4321
  - [ ] final subtask cc @mention
- [x] a separate task


#### References

* SHA: dbcd7a410ee7489acf92f40641a135fbcf52a768
* User@SHA: joeyespo@dbcd7a410ee7489acf92f40641a135fbcf52a768
* User/Repository@SHA: joeyespo/grip@dbcd7a410ee7489acf92f40641a135fbcf52a768
* #Num: #135
* GH-Num: GH-135
* User#Num: joeyespo#135
* User/Repository#Num: joeyespo/grip#135
